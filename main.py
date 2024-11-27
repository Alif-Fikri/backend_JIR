from fastapi import FastAPI
from auth.routes import router as auth_router
from users.routes import router as users_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti "*" dengan domain frontend jika sudah deploy
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua metode (GET, POST, OPTIONS, dll.)
    allow_headers=["*"],  # Izinkan semua header
)

app.include_router(auth_router)
app.include_router(users_router)
