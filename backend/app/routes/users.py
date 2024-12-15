# backend/app/routes/users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UserOut
from app.models import UserModel
from app.dependencies import get_current_user_id

router = APIRouter()

@router.get("/", response_model=list[UserOut])
def get_users(current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    users = db.query(UserModel).filter(UserModel.id != current_user_id).all()
    return users
