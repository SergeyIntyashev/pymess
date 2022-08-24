from uuid import UUID

from app.repositories.users import UsersRepository
from app.schemes.messengers import User, RoomInDB, BlockUserInfo
from app.tools.security import query_user_matching_check
from fastapi import APIRouter, Depends, status, Request
from loguru import logger

router = APIRouter()


@router.get('/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, users: UsersRepository = Depends()):
    result = await users.find_by_id(user_id)

    return User.from_orm(result)


@router.get('/rooms/{user_id}', response_model=list[RoomInDB],
            status_code=status.HTTP_200_OK)
async def get_all_user_rooms(request: Request, user_id: UUID,
                             users: UsersRepository = Depends()):
    query_user_matching_check(request, user_id)

    result = await users.find_all_user_rooms(user_id)

    return [RoomInDB.from_orm(room) for room in result]


@router.post('/block', status_code=status.HTTP_201_CREATED)
async def block_user(request: Request, data: BlockUserInfo,
                     users: UsersRepository = Depends()):
    query_user_matching_check(request, data.owner_id)

    await users.block_user(data)
    logger.info(f"User with id {data.user_id} successfully blocked "
                f"by user with id {data.owner_id}")


@router.post('/unblock', status_code=status.HTTP_200_OK)
async def unblock_user(request: Request, data: BlockUserInfo,
                       users: UsersRepository = Depends()):
    query_user_matching_check(request, data.owner_id)

    await users.unblock_user(data)
    logger.info(f"User with id {data.user_id} successfully unblocked "
                f"by user with id {data.owner_id}")
