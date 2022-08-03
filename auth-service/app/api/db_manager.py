from db import users, database
from models import UserInDB


async def add_user(payload: UserInDB):
    query = users.insert().values(**payload.dict())
    return await database.execute(query=query)


async def get_user_by_username(username: str):
    query = users.select(users.c.username == username)
    return await database.fetch_one(query=query)
