import asyncio
from functools import lru_cache

from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    KAFKA_HOST_URL: str
    KAFKA_TOPIC: str = "messages"
    KAFKA_PREMIUM_TOPIC: str = "premium-messages"
    KAFKA_CONSUMER_GROUP: str = "sender-group"

    class Config:
        env_file = '.env'


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
        return f"{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}" \
               f":{self.DB_PORT}/{self.DB_TITLE}"

    @property
    def db_uri(self) -> str:
        return f"postgresql://{self._db_domain}"


class ServiceHosts(BaseSettings):
    AUTH_SERVICE_HOST_URL: str

    class Config:
        env_file = '.env'


@lru_cache
def get_kafka_settings() -> tuple[KafkaSettings, any]:
    return KafkaSettings(), asyncio.get_event_loop()


@lru_cache
def get_db_settings() -> DBSettings:
    return DBSettings()


@lru_cache
def get_service_hosts() -> ServiceHosts:
    return ServiceHosts()


kafka_settings, loop = get_kafka_settings()

db_settings = get_db_settings()

service_hosts = get_service_hosts()
