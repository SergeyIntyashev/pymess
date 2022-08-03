from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class User(BaseModel):
    username: str
    fullname: str | None = None
    is_active: bool = True


class UserIn(User):
    password: str


class UserInDB(User):
    hashed_password: str
