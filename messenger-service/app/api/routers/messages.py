from uuid import UUID

from app.repositories.messages import MessagesRepository
from app.schemes.messengers import MessageUpdate
from fastapi import APIRouter, Depends, status, Request, HTTPException
from loguru import logger

router = APIRouter()


@router.delete('/{message_id}', status_code=status.HTTP_200_OK)
async def delete_message(request: Request, message_id: UUID,
                         messages: MessagesRepository = Depends()):
    message = await messages.find_by_id(message_id)
    if message.sender_id is not request.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't perform this action"
        )

    await messages.delete(message_id)

    logger.info(f"User with id {message.sender_id} delete message "
                f"with id {message.id} in room with id {message.room_id}")


@router.patch(status_code=status.HTTP_200_OK)
async def update_message(request: Request, payload: MessageUpdate,
                         messages: MessagesRepository = Depends()):
    message = await messages.find_by_id(payload.id)
    if message.sender_id is not request.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't perform this action"
        )

    await messages.update(payload)

    logger.info(f"User with id {message.sender_id} delete message "
                f"with id {message.id} in room with id {message.room_id}")
