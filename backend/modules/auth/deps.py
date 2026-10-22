from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_async_session
from database.models import Users

from modules.auth.repository import AuthRepo
from modules.auth.service import AuthService
from modules.companies.deps import get_company_repo
from modules.companies.repo import CompanyRepo
from utils.logger import logger


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

async def get_current_member(
        user: Users = Depends(get_current_user),
        service: AuthService = Depends(get_auth_service)
):
    return await service.check_member(user)

async def check_exists_company_id(
    company_id: int, repo: CompanyRepo = Depends(get_company_repo)
) -> int:
    company = await repo.get_company_by_id(company_id)
    if company is None:
        logger.warning("Not found company {}", company_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )

    return company.id


refresh_security = HTTPBearer(scheme_name="Refresh Bearer")


@dataclass(frozen=True)
class RefreshTokenContext:
    token: str
    user: Users


async def get_current_user_refresh_token(
        credentials: HTTPAuthorizationCredentials = Depends(refresh_security),
        service: AuthService = Depends(get_auth_service)
) -> RefreshTokenContext:
    user = await service.check_refresh_token(credentials.credentials)
    return RefreshTokenContext(
        token=credentials.credentials,
        user=user
    )
