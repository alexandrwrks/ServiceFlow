from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Orders
from modules.order.repo import OrderRepo
from modules.order.service import OrderService
from database.config import get_async_session


async def get_order_service(session: AsyncSession = Depends(get_async_session)) -> OrderService:
    return OrderService(session)


async def get_order_repo(session: AsyncSession = Depends(get_async_session)) -> OrderRepo:
    return OrderRepo(session)


async def check_exists_order_id(
        order_id: int,
        repo: OrderRepo = Depends(get_order_repo)
) -> Orders:
    order = await repo.get_by_id(order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order


ExistsOrder = Annotated[Orders, Depends(check_exists_order_id)]