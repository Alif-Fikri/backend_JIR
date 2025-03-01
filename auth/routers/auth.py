from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from auth.database import get_db
from auth.models.user import BlacklistedToken, User
from auth.schemas.user import (
    UserCreate,
    UserGoogleCreate,
    UserLogin,
    Token,
    UserResponse,
    ChangePasswordRequest
)
from auth.crud.user import (
    get_user_by_email,
    create_user,
    verify_password,
    get_password_hash,
    blacklist_token
)
from auth.dependencies import get_current_user, oauth2_scheme
from auth.utils import create_access_token
from auth.database import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["hashed_password"] = hashed_password
    del user_data["password"]
    
    return create_user(db, user_data)

@router.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.email)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/google/login", response_model=Token)
async def google_login(
    google_data: UserGoogleCreate, 
    db: Session = Depends(get_db)
):
    try:
        # Verifikasi token Google
        id_info = id_token.verify_oauth2_token(
            google_data.id_token,
            requests.Request(),
            audience=settings.GOOGLE_CLIENT_ID  
        )

        # Validasi email
        if not id_info.get("email_verified", False):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email not verified by Google"
            )

        email = id_info.get("email")
        name = id_info.get("name", "User")  
        google_id = id_info.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Google token"
            )
        user = get_user_by_email(db, email)
        if not user:
            user_data = {
                "email": email,
                "username": name,
                "google_id": google_id,
                "is_active": True
            }
            
            existing_user = get_user_by_email(db, email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered with regular signup"
                )
                
            user = create_user(db, user_data)
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    blacklist_token(db, token)
    return {"message": "Successfully logged out"}

@router.delete("/delete-account")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Hapus user dari database
    db.delete(current_user)
    db.commit()
    
    # Optional: Hapus semua token user tersebut dari blacklist
    # db.query(BlacklistedToken).filter(BlacklistedToken.token.in_(user_tokens)).delete()
    # db.commit()
    
    return {"message": "Account deleted successfully"}

@router.put("/change-password")
def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )
    
    new_hashed_password = get_password_hash(password_data.new_password)
    current_user.hashed_password = new_hashed_password
    db.commit()
    
    return {"message": "Password changed successfully"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user