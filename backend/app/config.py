# backend/app/config.py

import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/appdb")
    KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # Adjusted from JWT_SECRET
    ALGORITHM = "HS256"  # Adjusted from JWT_ALGORITHM

# Creating an instance of Settings
settings = Settings()
