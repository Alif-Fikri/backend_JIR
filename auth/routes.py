import logging
from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from database import db
from auth.utils import create_access_token
from pydantic import BaseModel, EmailStr
from auth.models import SignupRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    return {"message": "User created successfully"}

@router.post("/login")
async def login(request: LoginRequest):
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Request data: {request}")
    
    try:
        users_collection = db["users"]
        user = users_collection.find_one({"email": request.email})
        
        if not user or not pwd_context.verify(request.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        token = create_access_token(data={"sub": user["email"]})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logging.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

