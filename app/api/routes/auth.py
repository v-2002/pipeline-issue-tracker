from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.core import security

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.post("/login")
#old login endpoint that accepted UserLogin schema with username and password fields.
#def login(user_data: UserLogin, db: Session = Depends(get_db)):
#    user = authenticate_user(db, user_data.username, user_data.password)
#
#New Login endpoint that uses OAuth2PasswordRequestForm, which is a standard way to handle form data for authentication in FastAPI.
#
#Changes made 
#OAuth2PasswordRequestForm replaces UserLogin — this reads form data instead of JSON
#Depends() on the form — FastAPI handles parsing automatically
#form_data.username and form_data.password instead of user_data
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = security.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}