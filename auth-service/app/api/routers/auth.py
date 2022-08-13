from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

from core.dependencies import get_current_active_user
from repositories.users import UsersRepository
from schemes.schemes import UserIn, UserInDB, User, Token
from utils.crypt import Crypter, get_crypter
from utils.security import Security, get_security

router = APIRouter()


@router.post('/sign-up', response_model=User, status_code=status.HTTP_201_CREATED)
async def sign_up(payload: UserIn, users: UsersRepository = Depends(), crypter: Crypter = Depends(get_crypter)):
    if _ := await users.find_by_username(payload.username):
        logger.info("User with username {username} already existed", username=payload.username)
        raise HTTPException(status_code=400, detail="Username already existed")

    hashed_password = crypter.get_password_hash(payload.password)

    new_user = UserInDB(
        **payload.dict(),
        id=uuid4(),
        hashed_password=hashed_password
    )

    await users.create(new_user)

    return User.from_orm(new_user)


@router.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), security: Security = Depends(get_security)):
    if not (user := await security.authenticate_user(username=form_data.username, password=form_data.password)):
        logger.info("Failed login attempt for username {username}", username=form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.crypter.create_access_token(
        data={"sub": user.username}
    )

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
