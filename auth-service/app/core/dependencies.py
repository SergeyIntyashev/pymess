from fastapi import Depends, HTTPException
from loguru import logger

from schemes.schemes import User
from utils.security import security


async def get_current_active_user(current_user: User = Depends(security.get_current_user)) -> User:
    if not current_user.is_active:
        logger.warning("Attempt to authenticate an inactive user")
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
