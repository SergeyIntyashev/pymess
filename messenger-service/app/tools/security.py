from datetime import datetime
from uuid import UUID

import aiohttp
from app.core.config import service_hosts
from app.repositories.rooms import RoomsRepository
from app.repositories.users import UsersRepository
from app.schemes.messengers import BlockUserInfo
from fastapi import HTTPException, status, Request
from fastapi_auth_middleware import FastAPIUser
from loguru import logger

bad_req_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="You can't perform this action"
)


async def verify_authorization_header() -> tuple[list[str], FastAPIUser]:
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

                user = FastAPIUser(
                    first_name=result['username'],
                    last_name=result['email'],
                    user_id=result['id']
                )

                return [], user
            else:
                logger.warning("Attempt unauthorized")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )


async def user_is_room_admin_check(room_id: UUID, user_id: UUID,
                                   rooms: RoomsRepository) -> None:
    room = await rooms.find_by_id(room_id)
    if room.admin is not user_id:
        logger.warning(f"Attempt to perform an action without being a room "
                       f"administrator by user with id {user_id}")

        raise bad_req_exception


def query_user_matching_check(request: Request, user_id: UUID) -> None:
    if request.user.id is not user_id:
        logger.warning(f"Attempt to perform an action on another user "
                       f"by user with id {user_id}")

        raise bad_req_exception


async def user_in_room_check(user_id: UUID, room_id: UUID,
                             rooms: RoomsRepository):
    if not await rooms.find_member_by_id(member_id=user_id, room_id=room_id):
        logger.warning("Attempt to send a message without being in the room")
        raise bad_req_exception


async def block_user_check(owner_id: UUID, user_id: UUID,
                           users: UsersRepository) -> None:
    block_user_info = BlockUserInfo(owner_id=owner_id, user_id=user_id)
    if result := await users.find_blocked_user(block_user_info):
        if result.expiration_time > datetime.now():
            logger.info(f"Attempt sending message to blocked "
                        f"user with id {owner_id} by user with id {user_id}")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are blacklisted by the user "
                       "and cannot send messages to him"
            )
