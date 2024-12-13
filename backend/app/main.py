# backend/app/main.py

from fastapi import FastAPI
from app.db import Base, engine
from app.routes import auth, messages
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WhatsApp Clone API", version="1.0")

@app.on_event("startup")
def startup_event():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")

app.include_router(auth.router)
app.include_router(messages.router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the WhatsApp Clone API"}
