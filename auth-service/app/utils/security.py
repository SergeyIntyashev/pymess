from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from loguru import logger

from ..utils.crypt import crypter
from ..repositories.users import UsersRepository
from ..schemes.schemes import User, TokenData


class Security:
    def __init__(self):
        self._users = UsersRepository()
        self._crypter = crypter

    async def authenticate_user(self, username: str, password: str) -> User or bool:
        if not (db_user := await self._users.find_by_username(username=username)):
            logger.info("User with username {username} not found", username=username)
            return False

        if not self._crypter.verify_password(plain_password=password, hashed_password=db_user.hashed_password):
            logger.warning("Failed password verification by {username}", username=username)
            return False

        return User.from_orm(db_user)

    async def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            claims = self._crypter.decode_access_token(token=token)

            if not (username := claims.get("sub")):
                logger.warning("Token claims does not contains sub")
                raise credentials_exception

            token_data = TokenData(username=username)
        except JWTError as exc:
            logger.warning("Error decrypting token")
            raise credentials_exception from exc

        if not (db_user := await self._users.find_by_username(username=token_data.username)):
            logger.info("User with username {username} not found", username=token_data.username)
            raise credentials_exception

        return User.from_orm(db_user)

    @property
    def crypter(self):
        return self._crypter


def get_security() -> Security:
    return Security()


security = get_security()
