# backend/app/routes/messages.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import MessageCreate, MessageOut
from app.models import MessageModel
from app.security import decode_token
from app.kafka_utils import produce_message
from app.websocket_manager import manager
from app.dependencies import get_current_user_id
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/", response_model=MessageOut)
async def send_message(
    msg: MessageCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
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
    logger.info(f"Message from user {user_id} to user {msg.recipient_id} sent and published to Kafka")

    # Créer l'événement WebSocket pour le nouveau message
    new_message_event = {
        "type": "new_message",
        "data": message_data
    }

    # Envoyer l'événement au destinataire
    await manager.send_personal_message(new_message_event, msg.recipient_id)
    # Optionnel : Envoyer l'événement à l'expéditeur (pour confirmation)
    await manager.send_personal_message(new_message_event, user_id)

    return new_msg

@router.get("/conversations/{user_id}", response_model=list[MessageOut])
def get_conversations(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    msgs = db.query(MessageModel).filter(
        (MessageModel.sender_id == user_id) | (MessageModel.recipient_id == user_id)
    ).order_by(MessageModel.timestamp.asc()).all()
    logger.info(f"Retrieved conversations for user {user_id}")
    return msgs
