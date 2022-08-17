from uuid import UUID

from app.db.database import database
from app.db.tables import rooms, users, users_rooms
from app.schemes.messengers import RoomInDB
from sqlalchemy import and_


class RoomsRepository:

    async def create(self, room: RoomInDB):
        query = rooms.create(**room.dict())
        return await database.execute(query=query)

    async def detele(self, room_id: UUID):
        query = rooms.delete(rooms.c.id == room_id)
        return await database.execute(query=query)

    async def update(self, room: RoomInDB):
        query = rooms.update().where(rooms.c.id == room.id) \
            .values(title=room.title)
        return await database.execute(query=query)

    async def delete_members(self, room_id: UUID, member_ids: list[UUID]):
        condition = and_(users_rooms.c.user_id.in_(member_ids),
                         users_rooms.c.room_id == room_id)
        query = users_rooms.filter(condition).delete()
        return await database.execute(query=query)

    async def add_members(self, room_id: UUID, member_ids: list[UUID]):
        values = [{'room_id': room_id, 'user_id': member_id}
                  for member_id in member_ids]
        query = users_rooms.create(values)
        return await database.execute(query=query)

    async def find_by_title(self, title: str):
        query = rooms.select(rooms.c.title == title)
        return await database.fetch_one(query=query)

    async def find_by_id(self, room_id: UUID):
        query = rooms.select(rooms.c.id == room_id)
        return await database.fetch_one(query=query)

    async def find_all_members(self, room_id: UUID):
        query = users.select().join_from(users_rooms, users,
                                         users_rooms.c.user_id == users.c.id,
                                         users_rooms.c.room_id == room_id)
        return await database.fetch_all(query=query)
