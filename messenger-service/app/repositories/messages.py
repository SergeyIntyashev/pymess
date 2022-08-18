from uuid import UUID

from app.db.database import database
from app.db.tables import messages
from app.schemes.messengers import MessageInDB, MessageFindSettings, MessageUpdate
from sqlalchemy import and_


class MessagesRepository:

    async def create(self, message: MessageInDB):
        query = messages.create(**message.dict())
        return await database.execute(query=query)

    async def delete(self, message_id: UUID):
        query = messages.delete(messages.c.id == message_id)
        return await database.execute(query=query)

    async def update(self, message: MessageUpdate):
        query = messages.update().where(messages.c.id == message.id). \
            values(content=message.content)
        return await database.execute(query=query)

    async def find_by_id(self, message_id: UUID):
        query = messages.select(messages.c.id == message_id)
        return await database.fetch_one(query=query)

    async def find_all_by_room(self, settings: MessageFindSettings):
        room_condition = messages.c.room_id == settings.room_id

        condition = room_condition \
            if settings.is_premium_user \
            else and_(room_condition, not messages.c.is_premium)

        query = messages.select().where(condition) \
            .slice(settings.start, settings.stop)
        return await database.fetch_all(query=query)
