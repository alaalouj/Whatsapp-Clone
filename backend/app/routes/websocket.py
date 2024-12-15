# backend/app/routes/websocket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import UserModel
from app.security import decode_token
from app.websocket_manager import manager  # Importer l'instance globale
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    logger.info(f"Attempting to connect WebSocket with token: {token}")
    try:
        payload = decode_token(token)
        if not payload:
            logger.error("Token decode failed")
            await websocket.close(code=1008)
            return

        user_id = int(payload.get("sub"))
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            logger.error(f"User with ID {user_id} not found")
            await websocket.close(code=1008)
            return

        await manager.connect(user_id, websocket)  # Utiliser l'instance globale
        logger.info(f"WebSocket connection established for user {user_id}")

        while True:
            data = await websocket.receive_text()
            # Vous pouvez gérer des messages entrants ici si nécessaire
            logger.info(f"Received message from user {user_id}: {data}")

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)  # Utiliser l'instance globale
        logger.info(f"WebSocket disconnected for user {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close(code=1008)
