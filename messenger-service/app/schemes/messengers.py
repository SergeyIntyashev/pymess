from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


# USER
class UserBase(BaseModel):
    id: UUID
    username: str
    fullname: str | None = None


class UserIn(UserBase):
    old_password: str
    new_password: str


class User(UserBase):
    is_active: bool = True

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class BlockUserInfo(BaseModel):
    owner_id: UUID
    user_id: UUID
    expiration_time: datetime | None = None


# ROOM
class Room(BaseModel):
    title: str
    admin: UUID


class RoomInDB(Room):
    id: UUID


class RoomMembers(BaseModel):
    room_id: UUID
    members: list[User | UUID]


# MESSAGE
class Message(BaseModel):
    content: str
    sender_id: UUID
    recipient_id: UUID | None = None
    room_id: UUID


class MessageInDB(Message):
    id: UUID


class MessageFindSettings(BaseModel):
    room_id: UUID
    start: int
    stop: int
