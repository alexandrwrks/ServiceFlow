from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_async_session
from modules.telegram.service import TelegramService


async def get_telegram_service(
        session: AsyncSession = Depends(get_async_session)
):
    return TelegramService(session)