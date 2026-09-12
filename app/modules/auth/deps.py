from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_async_session
from app.database.models import Users

from app.modules.auth.repository import AuthRepo
from app.modules.auth.service import AuthService


async def get_auth_service(session: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(session)


async def get_auth_repo(session: AsyncSession = Depends(get_async_session)) -> AuthRepo:
    return AuthRepo(session)


access_security = HTTPBearer(scheme_name="Access Bearer")


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(access_security),
        service: AuthService = Depends(get_auth_service)
) -> Users:
    return await service.check_user(credentials.credentials)


async def check_owner_user(
        current_user: Users = Depends(get_current_user),
        service: AuthService = Depends(get_auth_service)
):
    return await service.check_owner_user(current_user)