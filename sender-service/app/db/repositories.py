from uuid import UUID

from app.db.database import database
from app.db.tables import rooms, users_rooms, blocked_users
from sqlalchemy import and_


class RoomsRepository:

    async def find_by_id(self, room_id: UUID):
        query = rooms.select(rooms.c.id == room_id)
        return await database.fetch_one(query=query)

    async def find_member_by_id(self, member_id: UUID, room_id: UUID):
        condition = and_(
            users_rooms.c.user_id == member_id,
            users_rooms.c.room_id == room_id
        )

        query = users_rooms.select(condition)
        return await database.fetch_one(query=query)


class UsersRepository:

    async def find_blocked_user(self, user_id: UUID, owner_id: UUID):
        condition = and_(
            blocked_users.c.user_id == user_id,
            blocked_users.c.owner_id == owner_id
        )

        query = blocked_users.select(condition)
        return await database.fetch_one(query=query)
