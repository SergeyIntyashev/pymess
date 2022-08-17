from functools import lru_cache

from pydantic import BaseSettings


class DBSettings(BaseSettings):
    """
    Class for storage connecting settings to database
    """
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


class ServiceHosts(BaseSettings):
    AUTH_SERVICE_HOST_URL: str
    SENDER_SERVICE_HOST_URL: str

    class Config:
        env_file = '.env'


@lru_cache
def get_db_settings() -> DBSettings:
    return DBSettings()


@lru_cache
def get_service_hosts() -> ServiceHosts:
    return ServiceHosts()


db_settings = get_db_settings()

service_hosts = get_service_hosts()
