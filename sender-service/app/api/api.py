from fastapi import APIRouter

from app.api.routers import sender

api_router = APIRouter()
api_router.include_router(sender.router)
