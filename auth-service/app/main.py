from app.api.api import auth
from app.db.database import database
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/auth/openapi.json",
              docs_url="/api/v1/auth/docs")

app.include_router(auth.router, prefix='/api/v1/auth', tags=["auth"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
