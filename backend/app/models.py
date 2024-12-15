# backend/app/models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  # Ajout de l'email
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    messages_sent = relationship("MessageModel", back_populates="sender", foreign_keys='MessageModel.sender_id')
    messages_received = relationship("MessageModel", back_populates="recipient", foreign_keys='MessageModel.recipient_id')

class MessageModel(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="sent")

    # Relations
    sender = relationship("UserModel", back_populates="messages_sent", foreign_keys=[sender_id])
    recipient = relationship("UserModel", back_populates="messages_received", foreign_keys=[recipient_id])
