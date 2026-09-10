from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.order.service import OrderService
from app.database.config import get_async_session


async def get_order_service(session: AsyncSession = Depends(get_async_session)):
    return OrderService(session)
