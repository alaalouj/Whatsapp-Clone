from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.db import engine, Base
from app.kafka_utils import start_kafka_consumer
from app.config import settings

app = FastAPI(title="WhatsApp Clone API", version="1.0")

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines pour simplifier le développement
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes
    allow_headers=["*"],  # Autoriser tous les headers
)

# Créer les tables de la base de données
Base.metadata.create_all(bind=engine)

# Inclure le routeur global
app.include_router(router)

# Démarrer le consommateur Kafka lors de l'événement de démarrage
@app.on_event("startup")
async def startup_event():
    start_kafka_consumer()
