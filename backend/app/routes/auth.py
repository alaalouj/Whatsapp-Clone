# backend/app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UserOut, UserCreate, UserLogin
from app.models import UserModel
from app.security import verify_password, create_access_token, get_password_hash

router = APIRouter()

@router.post("/users/register", response_model=UserOut)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user_data.password)
    new_user = UserModel(
        username=user_data.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/users/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserOut)
def get_me(token: str = Header(None), db: Session = Depends(get_db)):
    from app.routes.messages import get_current_user_id
    user_id = get_current_user_id(token=token, db=db)
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
