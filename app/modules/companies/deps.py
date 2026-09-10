from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.companies.repo import CompanyRepo
from app.modules.companies.service import CompanyService
from app.cache.cache_service import CacheService
from app.database.config import get_async_session
from app.cache.redis import redis
from app.database.models import Companies
from app.utils.logger import logger


async def get_cache_service() -> CacheService:
    return CacheService(redis)


async def get_company_service(
    session: AsyncSession = Depends(get_async_session),
    cache: CacheService = Depends(get_cache_service),
):
    return CompanyService(session, cache)


async def get_company_repo(session: AsyncSession = Depends(get_async_session)):
    return CompanyRepo(session)


async def check_exists_company_id(
    company_id: int, repo: CompanyRepo = Depends(get_company_repo)
) -> Companies:
    company = await repo.get_company_by_id(company_id)
    if company is None:
        logger.warning("Not found company {}", company_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )

    return company
