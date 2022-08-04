from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.models import UserIn, UserInDB, Token, User

from app.api.security import get_password_hash, authenticate_user, create_access_token, get_current_active_user
from app.api.db_manager import get_user_by_username, add_user

auth = APIRouter()


@auth.post('/sign-up')
async def sign_up(payload: UserIn):
    db_user = await get_user_by_username(payload.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already existed")
    hashed_password = get_password_hash(payload.password)
    new_user = UserInDB(username=payload.username,
                        fullname=payload.fullname,
                        is_active=payload.is_active,
                        hashed_password=hashed_password)
    return await add_user(new_user)


@auth.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
