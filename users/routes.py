from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.utils import verify_access_token
from .services import get_user_by_email, delete_user_by_email, update_user_password
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    email = payload.get("sub")
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/delete")
async def delete_account(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    email = payload.get("sub")
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    delete_user_by_email(email)
    return {"message": "Account deleted successfully"}

@router.put("/change-password")
async def change_password(
    old_password: str, 
    new_password: str, 
    token: str = Depends(oauth2_scheme)
):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    email = payload.get("sub")
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not pwd_context.verify(old_password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Old password is incorrect")
    
    hashed_new_password = pwd_context.hash(new_password)
    update_user_password(email, hashed_new_password)
    return {"message": "Password changed successfully"}

