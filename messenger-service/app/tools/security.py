from uuid import UUID

import aiohttp
from app.core.config import service_hosts
from app.repositories.rooms import RoomsRepository
from fastapi import HTTPException, status
from fastapi_auth_middleware import FastAPIUser
from loguru import logger


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


async def check_user_is_room_admin(room_id: UUID, user_id: UUID,
                                   rooms: RoomsRepository):
    room = await rooms.find_by_id(room_id)
    if room.admin is not user_id:
        logger.info(f"Attempt to delete a non-own room "
                    f"by user with id {user_id}")

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't delete a room that doesn't belong to you"
        )
