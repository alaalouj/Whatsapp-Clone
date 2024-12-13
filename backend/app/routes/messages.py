# backend/app/routes/messages.py

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import MessageCreate, MessageOut
from app.models import UserModel, MessageModel
from app.security import decode_token
from app.kafka_utils import produce_message
import asyncio

router = APIRouter()

def get_current_user_id(token: str = Header(None), db: Session = Depends(get_db)):
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user_id

@router.post("/messages", response_model=MessageOut)
async def send_message(msg: MessageCreate, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # Insérer en BDD
    new_msg = MessageModel(
        sender_id=user_id,
        recipient_id=msg.recipient_id,
        content=msg.content
    )
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)

    # Publier sur Kafka
    message_data = {
        "sender_id": user_id,
        "recipient_id": msg.recipient_id,
        "content": msg.content,
        "timestamp": str(new_msg.timestamp)
    }
    await produce_message("messages", message_data)

    return new_msg

@router.get("/conversations/{user_id}", response_model=list[MessageOut])
def get_conversations(user_id: int, current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    msgs = db.query(MessageModel).filter(
        (MessageModel.sender_id == user_id) | (MessageModel.recipient_id == user_id)
    ).order_by(MessageModel.timestamp.asc()).all()
    return msgs
