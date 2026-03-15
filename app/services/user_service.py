from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user import UserCreate
from app.core import security

def create_user(db: Session, user_data: UserCreate):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail=f"User {user_data.username} already exists")
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=security.hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user