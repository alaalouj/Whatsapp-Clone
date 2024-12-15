# backend/app/websocket_manager.py

from typing import Dict, List
from fastapi import WebSocket
import logging

logger = logging.getLogger("websocket_manager")
logging.basicConfig(level=logging.INFO)

class ConnectionManager:
    def __init__(self):
        # Dictionnaire où la clé est l'ID utilisateur et la valeur est une liste de connexions WebSocket
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected via WebSocket")

    def disconnect(self, user_id: int, websocket: WebSocket):
        self.active_connections[user_id].remove(websocket)
        if not self.active_connections[user_id]:
            del self.active_connections[user_id]
        logger.info(f"User {user_id} disconnected from WebSocket")

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)
            logger.info(f"Sent message to user {user_id} via WebSocket")
        else:
            logger.info(f"No active WebSocket connections for user {user_id}")

    async def broadcast(self, message: dict):
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                await connection.send_json(message)
        logger.info("Broadcasted message to all users via WebSocket")

# Créez une instance globale de ConnectionManager
manager = ConnectionManager()
