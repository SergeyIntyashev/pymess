from functools import lru_cache

from app.repositories.messages import MessagesRepository


@lru_cache
def get_messages_repository() -> MessagesRepository:
    return MessagesRepository()


messages_repository = get_messages_repository()
