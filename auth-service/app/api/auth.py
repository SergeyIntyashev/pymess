from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models import UserIn

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
    return await db_manager.add_user(
        {'username': payload.username, 'fullname': payload.fullname, 'is_active': payload.is_active,
         'hashed_password': hashed_password})


@auth.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    pass
