from typing import List

from sqlalchemy import select, not_, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Orders, OrderHistoryStatus, OrderStatusType


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> Orders | None:
        result = await self.session.execute(
            select(Orders)
            .where(Orders.id == order_id)
        )

        return result.scalar_one_or_none()

    async def get_history(self, order_id: int) -> List[OrderHistoryStatus]:
        result = await self.session.execute(
            select(OrderHistoryStatus)
            .where(OrderHistoryStatus.order_id == order_id)
        )

        return result.scalars().all()

    async def get_orders(self):
        result = await self.session.execute(
            select(Orders)
            .where(not_(Orders.status == OrderStatusType.CLOSED))
        )

        return result.scalars().all()

    async def update_order_status(self, order_id: int, status: OrderStatusType):
        await self.session.execute(
            update(Orders)
            .values(status=status)
            .where(Orders.id == order_id)
        )