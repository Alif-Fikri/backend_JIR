from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_admin: bool = False

class UserInCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInResponse(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
