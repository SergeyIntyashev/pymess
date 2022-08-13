from time import time

from jose import jwt
from passlib.context import CryptContext

from app.core.config import jwt_settings


class Crypter:
    def __init__(self, secret_key: str, algorithm: str = 'HS256', expire_minutes: int = 60) -> None:
        self._context = CryptContext(schemes=["bcrypt"])
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def get_password_hash(self, password) -> str:
        return self._context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self._context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        claims_to_encode = data.copy()
        claims_to_encode.update({"exp": time() + self._expire_minutes})

        return jwt.encode(claims=claims_to_encode, key=self._secret_key, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> dict:
        return jwt.decode(token=token, key=self._secret_key, algorithms=[self._algorithm])


def get_crypter() -> Crypter:
    return Crypter(
        jwt_settings.JWT_SECRET_KEY,
        jwt_settings.ALGORITHM,
        jwt_settings.JWT_EXPIRE_MINUTES
    )


crypter = get_crypter()
