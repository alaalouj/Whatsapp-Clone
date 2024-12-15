# backend/app/kafka_utils.py

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer, errors
import asyncio
import json
from app.config import settings  # Import the settings instance
from app.websocket_manager import manager

async def produce_message(topic: str, message: dict):
    producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BROKER)  # Access via settings
    await producer.start()
    try:
        value = json.dumps(message).encode('utf-8')
        await producer.send_and_wait(topic, value)
    except Exception as e:
        print(f"Error producing message: {e}")
    finally:
        await producer.stop()

async def consume_messages():
    while True:
        try:
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
                    recipient_id = message_data.get("recipient_id")
                    if recipient_id:
                        await manager.send_personal_message(message_data, recipient_id)
            finally:
                await consumer.stop()
        except errors.KafkaConnectionError as e:
            print(f"Kafka connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

def start_kafka_consumer():
    loop = asyncio.get_event_loop()
    loop.create_task(consume_messages())
