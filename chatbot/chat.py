from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse, StreamingResponse
import torch
import json
import random
import io
import numpy as np
from gtts import gTTS
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

app = FastAPI()

with open("intents.json", "r", encoding="utf-8") as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE, map_location=torch.device('cpu'))  # Gunakan CPU jika tidak ada GPU

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"
last_response = ""
audio_cache = {}  # Cache audio untuk menghindari pembuatan ulang

# Model request untuk menerima data dari frontend
class ChatRequest(BaseModel):
    message: str

@app.post("/get_response")
async def get_response(request: ChatRequest):
    global last_response
    sentence = tokenize(request.message)
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
                last_response = random.choice(intent["responses"])
                return {"response": last_response}
    else:
        last_response = "Saya tidak mengerti..."
        return {"response": last_response}

@app.get("/get_audio")
async def get_audio():
    global last_response
    if last_response in audio_cache:
        # Jika audio sudah ada di cache, kirim ulang tanpa membuat ulang file
        return StreamingResponse(io.BytesIO(audio_cache[last_response]), media_type="audio/mpeg")

    tts = gTTS(text=last_response, lang="id")
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)

    # Simpan ke cache
    audio_cache[last_response] = audio_fp.getvalue()

    return StreamingResponse(io.BytesIO(audio_cache[last_response]), media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
