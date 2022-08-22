from uuid import uuid4, UUID

from app.repositories.messages import MessagesRepository
from app.repositories.rooms import RoomsRepository
from app.schemes.messengers import Room, RoomInDB, RoomMembers, User, MessageInDB, MessageFindSettings
from app.tools.security import user_is_room_admin_check, user_in_room_check
from fastapi import APIRouter, Depends, status, Request
from loguru import logger

router = APIRouter()


@router.post('/', response_model=RoomInDB, status_code=status.HTTP_201_CREATED)
async def create_room(request: Request, payload: Room,
                      rooms: RoomsRepository = Depends()):
    new_room = RoomInDB(
        **payload.dict(),
        id=uuid4(),
    )

    await rooms.create(new_room)
    logger.info(f"Successfully created room {new_room.title} "
                f"by username {request.user.first_name}")

    return new_room


@router.delete('/{room_id}', status_code=status.HTTP_200_OK)
async def delete_room(request: Request, room_id: UUID,
                      rooms: RoomsRepository = Depends()):
    await user_is_room_admin_check(room_id, request.user.id, rooms)

    await rooms.delete(room_id)
    logger.info(f"Successfully deleted room with id {room_id} "
                f"by username {request.user.first_name}")


@router.patch('/{room_id}', response_model=RoomInDB,
              status_code=status.HTTP_200_OK)
async def update_room(request: Request, room: RoomInDB,
                      rooms: RoomsRepository = Depends()):
    await user_is_room_admin_check(room.id, request.user.id, rooms)

    result = await rooms.update(room)
    logger.info(f"Successfully update room with id {room.id} "
                f"by username {request.user.first_name}")

    return RoomInDB.from_orm(result)


@router.get('/{room_id}', response_model=RoomInDB,
            status_code=status.HTTP_200_OK)
async def find_room_by_id(room_id: UUID, rooms: RoomsRepository = Depends()):
    result = await rooms.find_by_id(room_id)

    return RoomInDB.from_orm(result)


@router.get("/{room_id}/members", response_model=RoomMembers,
            status_code=status.HTTP_200_OK)
async def find_all_members_by_room_id(request: Request, room_id: UUID,
                                      rooms: RoomsRepository = Depends()):
    await user_is_room_admin_check(room_id, request.user.id, rooms)

    result = await rooms.find_all_members(room_id)

    return RoomMembers(
        room_id=room_id,
        members=[User.from_orm(user) for user in result]
    )


@router.post('/members', status_code=status.HTTP_201_CREATED)
async def add_members_to_room(request: Request, room_members: RoomMembers,
                              rooms: RoomsRepository = Depends()):
    await user_is_room_admin_check(room_members.room_id, request.user.id, rooms)

    await rooms.add_members(room_members)
    logger.info(f"Successfully added {len(room_members.members)} members "
                f"to room with id {room_members.room_id} "
                f"by username {request.user.first_name}")


@router.delete('/members', status_code=status.HTTP_200_OK)
async def delete_members_from_room(request: Request, room_members: RoomMembers,
                                   rooms: RoomsRepository = Depends()):
    await user_is_room_admin_check(room_members.room_id, request.user.id, rooms)

    await rooms.delete_members(room_members)
    logger.info(f"Successfully deleted {len(room_members.members)} members "
                f"from room with id {room_members.room_id} "
                f"by username {request.user.first_name}")


@router.get('/{room_id}/all')
async def get_all_message(request: Request, room_id: UUID,
                          start: int = 0, stop: int = 30,
                          rooms: RoomsRepository = Depends(),
                          messages: MessagesRepository = Depends()):
    await user_in_room_check(request.user.id, room_id, rooms)

    query_settings = MessageFindSettings(
        room_id=room_id,
        start=start,
        stop=stop,
        is_premium_user=request.user.is_premium
    )
    result = await messages.find_all_by_room(query_settings)

    return [MessageInDB.from_orm(message) for message in result]
