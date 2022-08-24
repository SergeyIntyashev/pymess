from app.api.api import sender
from app.api.routers.sender import producer
from app.db.database import database
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/sender/openapi.json",
              docs_url="/api/v1/auth/sender")

app.include_router(sender.router, prefix='/api/v1/sender', tags=["sender"])


@app.on_event("startup")
async def startup():
    await database.connect()
    await producer.start()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await producer.stop()
