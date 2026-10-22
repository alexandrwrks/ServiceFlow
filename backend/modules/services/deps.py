from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_async_session
from database.models import Services, StatusType
from modules.services.repository import ProviderRepo
from modules.services.service import ProviderService


async def get_provider_service(session: AsyncSession = Depends(get_async_session)):
    return ProviderService(session)


async def get_provider_repo(session: AsyncSession = Depends(get_async_session)) -> ProviderRepo:
    return ProviderRepo(session)


def check_service_status_type(*status_types):
    async def check_service_id(
            service_id: int,
            repo: ProviderRepo = Depends(get_provider_repo)
    ) -> Services:
        exist_service = await repo.get_service_by_id(service_id)
        if exist_service is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        if exist_service.active not in status_types:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "SERVICE_INACTIVE",
                    "message": "This service is currently inactive"
                }
            )

        return exist_service
    return check_service_id