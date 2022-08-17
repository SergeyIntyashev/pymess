import aiohttp
from app.core.config import service_hosts
from fastapi import HTTPException, status
from fastapi_auth_middleware import FastAPIUser


async def verify_authorization_header() -> tuple[list[str], FastAPIUser]:
    async with aiohttp.ClientSession() as session:
        get_user_uri = f"{service_hosts.AUTH_SERVICE_HOST_URL}/me"
        async with session.get(get_user_uri) as response:
            if response.status == 200:
                result = await response.json()
                user = FastAPIUser(
                    first_name=result['username'],
                    last_name=result['email'],
                    user_id=result['id']
                )
                return [], user
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
