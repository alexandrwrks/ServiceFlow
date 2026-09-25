from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_async_session
from app.modules.services.repository import ProviderRepo
from app.modules.services.service import ProviderService


async def get_provider_service(session: AsyncSession = Depends(get_async_session)):
    return ProviderService(session)


async def get_provider_repo(session: AsyncSession) -> ProviderRepo:
    return ProviderRepo(session)


async def check_service_id(
        service_id: int,
        repo: ProviderRepo = Depends(get_provider_repo)
):
    exist_service = await repo.get_service_by_id(service_id)
    if exist_service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )

    return exist_service