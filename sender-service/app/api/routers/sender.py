from aiokafka import AIOKafkaProducer
from app.core.config import kafka_settings, loop
from app.db.repositories import UsersRepository, RoomsRepository
from app.schemes.senders import Message
from app.utils.security import query_user_matching_check, user_in_room_check, \
    block_user_check
from fastapi import APIRouter, Depends, status, Request
from loguru import logger

router = APIRouter()


@router.post('send-message', status_code=status.HTTP_200_OK)
async def send_message(request: Request, message: Message,
                       users: UsersRepository = Depends(),
                       rooms: RoomsRepository = Depends()):
    # checkings user
    query_user_matching_check(request, message.sender_id)
    await user_in_room_check(message.sender_id, message.room_id, rooms)
    if message.recipient_id:
        await block_user_check(message.recipient_id, message.sender_id, users)

    producer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=kafka_settings.KAFKA_HOST_URL
    )

    await producer.start()
    try:
        value_json = message.json().encode('utf-8')
        topic = kafka_settings.KAFKA_PREMIUM_TOPIC if message.is_premium \
            else kafka_settings.KAFKA_TOPIC
        await producer.send_and_wait(topic=topic, value=value_json)
    finally:
        logger.info(f"Message from user with id {message.sender_id} "
                    f"sent to Kafka")
        await producer.stop()
