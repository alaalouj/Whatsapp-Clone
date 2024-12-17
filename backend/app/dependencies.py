# backend/app/dependencies.py

from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import UserModel
from app.security import decode_token
import logging

logger = logging.getLogger(__name__)

def get_current_user_id(authorization: str = Header(None), db: Session = Depends(get_db)) -> int:
    """
    Dépendance pour obtenir l'ID de l'utilisateur actuel à partir du token JWT.
    """
    if not authorization:
        logger.error("Authorization header missing")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    parts = authorization.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        logger.error(f"Invalid authorization header format: {authorization}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")

    token = parts[1]
    logger.debug(f"Token extracted: {token}")

    payload = decode_token(token)
    if not payload:
        logger.error("Token decode failed")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        logger.error("User ID (sub) missing in token payload")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    try:
        user_id = int(user_id)
    except ValueError:
        logger.error(f"Invalid user ID in token payload: {user_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID in token")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        logger.error(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    logger.debug(f"Authenticated user_id: {user_id}")
    return user_id


def get_current_username(authorization: str = Header(None), db: Session = Depends(get_db)) -> str:
    
    user_id = get_current_user_id(authorization, db)
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        logger.error(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    logger.debug(f"Authenticated username: {user.username}")
    return user.username
