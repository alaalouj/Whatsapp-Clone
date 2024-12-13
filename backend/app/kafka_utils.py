from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
import json
from app.config import KAFKA_BROKER

async def produce_message(topic: str, message: dict):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()
    try:
        value = json.dumps(message).encode('utf-8')
        await producer.send_and_wait(topic, value)
    finally:
        await producer.stop()

# Un consommateur pourrait être lancé dans un thread séparé ou une tâche async
# Ici, c'est un exemple. Dans un vrai cas, vous auriez un script séparé.
async def consume_messages(topic: str):
    consumer = AIOKafkaConsumer(topic, bootstrap_servers=KAFKA_BROKER, group_id="group1")
    await consumer.start()
    try:
        async for msg in consumer:
            data = json.loads(msg.value.decode('utf-8'))
            # Traiter le message (ex: mettre à jour statut en BDD)
    finally:
        await consumer.stop()
