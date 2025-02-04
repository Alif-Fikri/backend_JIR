import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from passlib.context import CryptContext
from database import db
from auth.utils import create_access_token, decode_access_token
from pydantic import BaseModel, EmailStr
from auth.models import SignupRequest, LoginRequest
from fastapi.security import OAuth2PasswordBearer
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
blacklisted_tokens = set()


@router.post("/google/callback")
async def google_callback(request: Request):
    body = await request.json()
    id_token_str = body.get("id_token")

    if not id_token_str:
        raise HTTPException(status_code=400, detail="ID Token is required")

    try:
        decoded_token = id_token.verify_oauth2_token(
            id_token_str, requests.Request()
        )
        email = decoded_token.get("email")
        name = decoded_token.get("name")
        google_id = decoded_token.get("sub")

        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")

        users_collection = db["users"]

        user = users_collection.find_one({"email": email})
        if not user:
            new_user = {
                "username": name,
                "email": email,
                "google_id": google_id,
                "is_active": True,
                "is_admin": False,
            }
            users_collection.insert_one(new_user)
            user = new_user

        # Buat token JWT untuk pengguna
        access_token = create_access_token(data={"sub": user["email"]})

        return {"access_token": access_token, "token_type": "bearer"}

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID Token")

@router.post("/signup")
async def signup(request: SignupRequest):
    users_collection = db["users"]

    if users_collection.find_one({"email": request.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(request.password)

    user = {
        "username": request.username,
        "email": request.email,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_admin": False,
    }
    users_collection.insert_one(user)

    # Generate token
    access_token = jwt.encode({"sub": request.email}, "secret_key", algorithm="HS256")
    
    return {"access_token": access_token, "message": "User created successfully"}

@router.post("/login")
async def login(request: LoginRequest):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Request payload: {request.dict()}")

    users_collection = db["users"]

    user = users_collection.find_one({"email": request.email})
    logging.debug(f"User retrieved: {user}")

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not pwd_context.verify(request.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Membuat token JWT
    token = create_access_token(data={"sub": user["email"]})
    logging.debug(f"Generated token: {token}")

    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Logout attempt for token: {token}")

    try:
        payload = decode_access_token(token)
        logging.debug(f"Token payload: {payload}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    blacklisted_tokens.add(token)
    return {"message": "Successfully logged out"}

def validate_token(token: str = Depends(oauth2_scheme)):

    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token has been invalidated")
    return token

