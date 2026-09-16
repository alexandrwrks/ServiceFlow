from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import OrderStatusType
from app.modules.order.repo import OrderRepo
from app.utils.logger import logger


class OrderService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = OrderRepo(session)

    async def get_order_history(self, order_id: int):
        order_history = await self.repo.get_history(order_id)
        return order_history

    async def get_orders(self):
        orders = await self.repo.get_orders()
        return orders

    async def complete_order(self, order_id: int):
        try:
            await self.repo.update_order_status(order_id, status=OrderStatusType.COMPLETED)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to complete order"
            )

        except Exception:
            logger.exception("Failed to complete order {}", order_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to complete order"
            )

    async def cancel_order(self, order_id: int):
        try:
            await self.repo.update_order_status(order_id, status=OrderStatusType.CANCELLED)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to cancel order"
            )

        except Exception:
            logger.exception("Failed to cancel order {}", order_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to cancel order"
            )

    async def assign_order(self, order_id: int):
        try:
            await self.repo.update_order_status(order_id, status=OrderStatusType.ASSIGNED)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to assign order"
            )

        except Exception:
            logger.exception("Failed to assign order {}", order_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to assign order"
            )

    async def confirm_order(self, order_id: int):
        try:
            await self.repo.update_order_status(order_id, status=OrderStatusType.CONFIRMED)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to confirm order"
            )

        except Exception:
            logger.exception("Failed to confirm order {}", order_id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to confirm order"
            )

    async def update_order_info(self, order_id: int, params):
        try:
            await self.repo.update_order_info(order_id, params)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to update order info"
            )