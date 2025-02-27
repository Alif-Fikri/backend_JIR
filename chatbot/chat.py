from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import io
import os
import torch
import json
import random
import numpy as np
from gtts import gTTS
from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words, tokenize

chat_router = APIRouter()  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r") as json_data:
    intents = json.load(json_data)

FILE = os.path.join(BASE_DIR, "data.pth")
data = torch.load(FILE, map_location=torch.device("cpu"))

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

device = torch.device("cpu")

bot_name = "Sam"
audio_cache = {}

class ChatRequest(BaseModel):
    message: str

@chat_router.post("/get_response") 
async def get_response(chat_request: ChatRequest):
    sentence = tokenize(chat_request.message)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = random.choice(intent["responses"])
                return {"response": response}
    else:
        return {"response": "Saya tidak mengerti..."}

@chat_router.get("/get_audio")  # Gunakan chat_router
async def get_audio(response_text: str):
    if response_text in audio_cache:
        return FileResponse(audio_cache[response_text], media_type="audio/mpeg")
    
    tts = gTTS(text=response_text, lang='id')
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    
    audio_cache[response_text] = audio_fp
    
    return FileResponse(audio_fp, media_type="audio/mpeg")
