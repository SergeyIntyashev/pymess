from functools import lru_cache

from pydantic import BaseSettings


class DBSettings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_TITLE: str

    class Config:
        env_file = '.env'

    @property
    def _db_domain(self) -> str:
        return f"{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_TITLE}"

    @property
    def db_uri(self) -> str:
        return f"postgresql://{self._db_domain}"


class JWTSettings(BaseSettings):
    JWT_EXPIRE_MINUTES: int = 60
    JWT_SECRET_KEY: str
    ALGORITHM: str = "HS256"

    class Config:
        env_file = '.env'


@lru_cache
def get_db_settings() -> DBSettings:
    return DBSettings()


@lru_cache
def get_jwt_settings() -> JWTSettings:
    return JWTSettings()
