from fastapi import FastAPI
from auth.routes import router as auth_router
from users.routes import router as users_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
