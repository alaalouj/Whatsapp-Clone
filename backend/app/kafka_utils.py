# backend/app/kafka_utils.py

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, errors
import asyncio
import json
from app.config import settings  # Import the settings instance
from app.websocket_manager import manager
import logging

logger = logging.getLogger("kafka_utils")
logging.basicConfig(level=logging.INFO)

async def produce_message(topic: str, message: dict):
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER)  # Access via settings
    await producer.start()
    try:
        value = json.dumps(message).encode('utf-8')
        await producer.send_and_wait(topic, value)
        logger.info(f"Produced message to Kafka topic '{topic}': {message}")
    except Exception as e:
        logger.error(f"Error producing message: {e}")
    finally:
        await producer.stop()

async def consume_messages():
    consumer = AIOKafkaConsumer(
        "messages",
        bootstrap_servers=settings.KAFKA_BROKER,  # Access via settings
        group_id="message-group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    await consumer.start()
    try:
        async for msg in consumer:
            message_data = msg.value
            logger.info(f"Consumed message from Kafka: {message_data}")
            recipient_id = message_data.get("recipient_id")
            if recipient_id:
                await manager.send_personal_message(message_data, recipient_id)
                logger.info(f"Sent message to user {recipient_id} via WebSocket")
    except errors.KafkaConnectionError as e:
        logger.error(f"Kafka connection error: {e}. Retrying in 5 seconds...")
        await asyncio.sleep(5)
        await consume_messages()
    except Exception as e:
        logger.error(f"Unexpected error: {e}. Retrying in 5 seconds...")
        await asyncio.sleep(5)
        await consume_messages()

def start_kafka_consumer():
    loop = asyncio.get_event_loop()
    loop.create_task(consume_messages())
    logger.info("Kafka consumer started")
