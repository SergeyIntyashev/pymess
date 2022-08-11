from fastapi import APIRouter

from .routers import auth

api_router = APIRouter()
api_router.include_router(auth.router)