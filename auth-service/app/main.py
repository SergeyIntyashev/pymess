from fastapi import FastAPI

from api.auth import auth
from api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/casts/docs")
app.include_router(auth, prefix='/api/v1/auth', tags=['auth'])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
