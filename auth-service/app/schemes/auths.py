from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    fullname: str | None = None


class UserIn(UserBase):
    password: str


class UserSemi(UserBase):
    is_active: bool = True


class User(UserSemi):
    id: UUID

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
