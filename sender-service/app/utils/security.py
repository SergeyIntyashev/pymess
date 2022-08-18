from datetime import datetime
from uuid import UUID

import aiohttp
from app.core.config import service_hosts
from app.db.repositories import RoomsRepository, UsersRepository
from app.schemes.senders import User
from fastapi import HTTPException, status, Request
from loguru import logger

bad_req_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="You can't perform this action"
)


async def verify_authorization_header() -> tuple[list[str], User]:
    async with aiohttp.ClientSession() as session:
        get_user_uri = f"{service_hosts.AUTH_SERVICE_HOST_URL}/me"
        async with session.get(get_user_uri) as response:
            if response.status == 200:
                result = await response.json()

                if not result.get('is_active', None):
                    logger.warning("Attempt to authenticate an inactive user")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Inactive user"
                    )

                return [], User.parse_raw(result)
            else:
                logger.warning("Attempt unauthorized")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )


def query_user_matching_check(request: Request, user_id: UUID) -> None:
    if request.user.id is not user_id:
        logger.warning(f"Attempt to perform an action on another user "
                       f"by user with id {user_id}")

        raise bad_req_exception


async def user_in_room_check(user_id: UUID, room_id: UUID,
                             rooms: RoomsRepository) -> None:
    if not await rooms.find_member_by_id(member_id=user_id, room_id=room_id):
        logger.warning("Attempt to send a message without being in the room")
        raise bad_req_exception


async def block_user_check(owner_id: UUID, user_id: UUID,
                           users: UsersRepository) -> None:
    if result := await users.find_blocked_user(user_id=user_id,
                                               owner_id=owner_id):
        if result.expiration_time > datetime.now():
            logger.info(f"Attempt sending message to blocked "
                        f"user with id {owner_id} by user with id {user_id}")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are blacklisted by the user "
                       "and cannot send messages to him"
            )
