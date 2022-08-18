import asyncio

from fastapi import FastAPI
from fastapi_auth_middleware import AuthMiddleware

from api import api
from core.message_queue_reader import read_messages_from_queue
from db.database import metadata, engine, database
from tools.security import verify_authorization_header

metadata.create_all(bind=engine)

app = FastAPI(openapi_url="/api/v1/messenger/openapi.json",
              docs_url="/api/v1/messenger/docs")

app.include_router(api.api_router, prefix='/api/v1/messenger', tags=["messenger"])
app.add_middleware(AuthMiddleware, verify_authorization_header=verify_authorization_header)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


asyncio.run(read_messages_from_queue())
