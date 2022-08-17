from uuid import UUID

from app.db.database import database
from app.db.tables import users, users_rooms, rooms, blocked_users
from app.schemes.messengers import UserInDB, BlockUserInfo
from sqlalchemy import and_


class UsersRepository:

    async def find_by_username(self, username: str):
        query = users.select(users.c.username == username)
        return await database.fetch_one(query=query)

    async def find_by_id(self, user_id: UUID):
        query = users.select(users.c.id == user_id)
        return await database.fetch_one(query=query)

    async def find_all_rooms(self, user_id: UUID):
        condition = and_(users_rooms.c.id == rooms.c.room_id,
                         users_rooms.c.user_id == user_id)
        query = rooms.select_from(users_rooms).select_from(
            users_rooms.join(rooms, condition))
        return await database.fetch_all(query=query)

    async def find_blocked_user(self, user_id: UUID, owner_id: UUID):
        query = blocked_users.select(blocked_users.c.user_id == user_id,
                                     blocked_users.c.owner_id == owner_id)
        return await database.fetch_one(query=query)

    async def block_user(self, data: BlockUserInfo):
        query = blocked_users.create(**data.dict())
        return await database.execute(query=query)

    async def unblock_user(self, user_id: UUID, owner_id: UUID):
        condition = and_(blocked_users.c.user_id == user_id,
                         blocked_users.c.owner_id == owner_id)
        query = blocked_users.filter(condition).delete()
        return await database.execute(query=query)
