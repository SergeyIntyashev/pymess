from fastapi import APIRouter

from app.api.routers import rooms, users, messages

api_router = APIRouter()
api_router.include_router(rooms.router)
api_router.include_router(users.router)
api_router.include_router(messages.router)
