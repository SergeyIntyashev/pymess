from app.db.database import database
from app.models.user import users
from app.schemes.auths import UserInDB


class UsersRepository:

    async def create(self, user: UserInDB):
        query = users.insert().values(**user.dict())
        return await database.execute(query)

    async def find_by_username(self, username: str):
        query = users.select(users.c.username == username)
        return await database.fetch_one(query=query)
