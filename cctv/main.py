from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
import cv2
import torch
from torchvision import transforms
from cctv.model import CSRNet
from PIL import Image
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import threading

cctv_router = APIRouter()  

# Inisialisasi model CSRNet
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
model = CSRNet().to(device)
checkpoint = torch.load('C:/Users/Alif Fikri/backend_JIR/cctv/weights.pth', map_location=device)
model.load_state_dict(checkpoint)
model.eval()

# Daftar URL CCTV
cctv_urls = {
    "DPR": "https://cctv.balitower.co.id/Bendungan-Hilir-003-700014_1/embed.html",
    "Bundaran HI": "https://cctv.balitower.co.id/Menteng-001-700123_5/embed.html",
    "Monas": "https://cctv.balitower.co.id/Monas-Barat-009-506632_2/embed.html",
    "Patung Kuda": "https://cctv.balitower.co.id/JPO-Merdeka-Barat-507357_9/embed.html",
}


chrome_driver_path = "C:/Users/Alif Fikri/backend_JIR/cctv/chromedriver-win64/chromedriver.exe"
driver_service = Service(chrome_driver_path)

latest_predictions = {location: {"predicted_count": 0} for location in cctv_urls.keys()}

def capture_and_predict(location, url):
    global latest_predictions
    driver = webdriver.Chrome(service=driver_service)
    driver.get(url)
    time.sleep(5)  
    while True:
        try:
            # Ambil screenshot
            driver.save_screenshot(f'screenshot_{location}.png')
            frame = cv2.imread(f'screenshot_{location}.png')

            # Convert ke PIL Image dan lakukan transformasi
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            img_tensor = transform(img).unsqueeze(0).to(device)

            # Prediksi menggunakan model
            with torch.no_grad():
                output = model(img_tensor)
            predicted_count = int(output.detach().cpu().sum().numpy())

            # Simpan hasil prediksi terbaru
            latest_predictions[location] = {"predicted_count": predicted_count}
            print(f"{location} Predicted Count:", predicted_count)

            # Tunggu beberapa detik sebelum mengambil screenshot berikutnya
            time.sleep(10)

        except Exception as e:
            print(f"Error in {location}: {e}")
            break

    driver.quit()

for location, url in cctv_urls.items():
    threading.Thread(target=capture_and_predict, args=(location, url), daemon=True).start()

@cctv_router.get("/get_predictions")
def get_predictions():
    return JSONResponse(content=latest_predictions)

