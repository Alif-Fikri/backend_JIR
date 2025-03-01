from fastapi import FastAPI
from auth.routers.auth import router as auth_router
from auth.database import init_db as init_auth_db
# from users.routes import router as users_router
from chatbot.chat import chat_router
# from cctv.main import cctv_router
# from cctv.main_video import cctv_video_router
from fastapi.middleware.cors import CORSMiddleware

init_auth_db()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua domain
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode (GET, POST, OPTIONS, dll.)
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(auth_router)
# app.include_router(users_router)
app.include_router(chat_router)
# app.include_router(cctv_router)
# app.include_router(cctv_video_router)
