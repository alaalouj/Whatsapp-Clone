import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/appdb")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_ALGORITHM = "HS256"

