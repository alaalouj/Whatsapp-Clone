# backend/app/routes/messages.py

from fastapi import APIRouter, Depends, HTTPException, Header, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import MessageCreate, MessageOut
from app.models import UserModel, MessageModel
from app.security import decode_token
from app.kafka_utils import produce_message
from app.websocket_manager import ConnectionManager
import asyncio

router = APIRouter()
manager = ConnectionManager()

def get_current_user_id(token: str = Header(None), db: Session = Depends(get_db)) -> int:
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
        "timestamp": new_msg.timestamp.isoformat()
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

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        if not payload:
            await websocket.close(code=1008)
            return
        user_id = int(payload.get("sub"))
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            await websocket.close(code=1008)
            return
        await manager.connect(user_id, websocket)
        while True:
            data = await websocket.receive_text()
            # Vous pouvez gérer des messages entrants si nécessaire
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
    except Exception as e:
        await websocket.close(code=1008)
