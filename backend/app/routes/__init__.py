# backend/app/routes/__init__.py

from fastapi import APIRouter

from .auth import router as auth_router
from .messages import router as messages_router
from .websocket import router as websocket_router
from .users import router as users_router  # Importer le router des utilisateurs

router = APIRouter()

router.include_router(auth_router, prefix="/users", tags=["Users"])
router.include_router(messages_router, prefix="/messages", tags=["Messages"])
router.include_router(websocket_router, prefix="", tags=["WebSocket"])
router.include_router(users_router, prefix="/users", tags=["Users"])  # Inclure le router des utilisateurs
