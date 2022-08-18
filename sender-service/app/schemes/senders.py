from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    fullname: str | None = None
    is_active: bool = True
    is_premium: bool = False

    class Config:
        orm_mode = True


class Message(BaseModel):
    content: str
    sender_id: UUID
    recipient_id: UUID | None = None
    room_id: UUID
    is_premium: bool = False
