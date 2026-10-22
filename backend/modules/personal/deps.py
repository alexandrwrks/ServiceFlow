from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_async_session
from modules.personal.service import PersonalService


async def get_personal_service(
        session: AsyncSession = Depends(get_async_session),
):
    return PersonalService(session)