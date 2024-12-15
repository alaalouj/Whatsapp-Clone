# backend/app/schemas.py

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john_doe@example.com")  # Ajout de l'email
    password: str = Field(..., example="strongpassword123")

class UserLogin(BaseModel):
    username: str = Field(..., example="john_doe")
    password: str = Field(..., example="strongpassword123")

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr  # Ajout de l'email
    created_at: datetime

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    recipient_id: int = Field(..., example=2)
    content: str = Field(..., example="Bonjour !")

class MessageOut(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    timestamp: datetime
    status: str

    class Config:
        orm_mode = True

class Conversation(BaseModel):
    user: UserOut
    messages: List[MessageOut]
