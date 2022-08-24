from uuid import uuid4

from aiokafka import AIOKafkaConsumer
from app.core.config import kafka_settings, loop
from app.core.tools import messages_repository
from app.schemes.messengers import MessageInDB
from loguru import logger


async def read_messages_from_queue():
    await consume(kafka_settings.KAFKA_TOPIC)
    await consume(kafka_settings.KAFKA_PREMIUM_TOPIC)


async def consume(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        loop=loop,
        bootstrap_servers=kafka_settings.KAFKA_HOST_URL,
        group_id=kafka_settings.KAFKA_CONSUMER_GROUP
    )

    await consumer.start()
    try:
        async for message in consumer:
            new_message = MessageInDB.parse_raw(message)
            new_message.id = uuid4()
            await messages_repository.create(new_message)
            logger.info(f"User with id {message.sender.id} send "
                        f"message in room with id {message.room_id}")
    finally:
        await consumer.stop()
