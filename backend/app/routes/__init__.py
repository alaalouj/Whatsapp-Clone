# backend/app/routes/__init__.py

from fastapi import APIRouter

from .auth import router as auth_router
from .messages import router as messages_router
from .websocket import router as websocket_router

router = APIRouter()

router.include_router(auth_router, prefix="/users", tags=["Users"])
router.include_router(messages_router, prefix="/messages", tags=["Messages"])
router.include_router(websocket_router, prefix="", tags=["WebSocket"])
