from app.api.api import sender
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/v1/sender/openapi.json",
              docs_url="/api/v1/auth/sender")

app.include_router(sender.router, prefix='/api/v1/sender', tags=["sender"])
