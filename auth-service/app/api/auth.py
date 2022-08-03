from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import UserIn, UserInDB

import security
import db_manager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth = APIRouter()


@auth.post('/sign-up')
async def sign_up(payload: UserIn):
    db_user = await db_manager.get_user_by_username(payload.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already existed")
    hashed_password = security.get_password_hash(payload.password)
    new_user = UserInDB(**payload, hashed_password=hashed_password)
    return await db_manager.add_user(new_user)


@auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass
