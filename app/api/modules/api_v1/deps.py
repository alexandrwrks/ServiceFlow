from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.modules.api_v1.service import CompanyService
from app.database.config import get_async_session


async def get_company_service(
        session: AsyncSession = Depends(get_async_session)
):
    return CompanyService(session)