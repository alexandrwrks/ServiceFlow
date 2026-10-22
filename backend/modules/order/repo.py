from datetime import timezone, datetime
from typing import List

from sqlalchemy import select, not_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user

from database.enum import OrderStatusType, StatusType
from database.models import Orders, OrderHistoryStatus, Services, CompanyMembers, Customers
from modules.order.schema import OrderParams


class OrderRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_by_id(self, order_id: int) -> Orders | None:
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

    async def get_orders(self, company_id: int) -> List[Orders]:
        result = await self.session.execute(
            select(Orders)
            .where(
                Orders.company_id == company_id,
                not_(Orders.status == OrderStatusType.CLOSED)
            )
        )

        return result.scalars().all()

    async def get_service_by_id(self, service_id: int) -> Services | None:
        result = await self.session.execute(
            select(Services)
            .where(
                Services.id == service_id,
                Services.active == StatusType.ACTIVE,
            )
        )

        return result.scalar_one_or_none()

    async def create_order(self, params: OrderParams, member: CompanyMembers) -> int:
        customer = await self.session.execute(
            insert(Customers)
            .values(
                full_name=f"{params.first_name} {params.last_name}",
                phone=params.phone,
            )
            .returning(Customers.id)
        )
        customer_id = customer.scalar_one()

        order = await self.session.execute(
            insert(Orders)
            .values(
                service_id=params.service_id,
                company_id=member.company_id,
                customer_id=customer_id,
                description=params.notes if params.notes is not None else None,
                created_by=member.id
            )
            .returning(Orders.id)
        )

        return order.scalar_one()

    async def get_by_id(self, order_id: int) -> Orders | None:
        result = await self.session.execute(
            select(Orders)
            .where(Orders.id == order_id)
        )

        return result.scalar_one_or_none()


    async def get_employee_by_id(self, employee_id: int) -> CompanyMembers | None:
        result = await self.session.execute(
            select(CompanyMembers)
            .where(CompanyMembers.id == employee_id)
        )

        return result.scalar_one_or_none()

    async def assigned_employee(self, order_id: int, employee_id: int):
        await self.session.execute(
            update(Orders)
            .where(Orders.id == order_id)
            .values(
                status=OrderStatusType.ASSIGNED,
                assigned_employee_id=employee_id
            )
        )

    async def get_for_update(self, order_id: int, company_id: int) -> Orders | None:
        result = await self.session.execute(
            select(Orders)
            .where(
                Orders.id == order_id,
                Orders.company_id == company_id,
            )
            .with_for_update()
            .execution_options(populate_existing=True)
        )

        return result.scalar_one_or_none()

    async def change_status(self, order_id: int, order: Orders, new_status: OrderStatusType, changed_by: int) -> None:
        old_status = order.status
        order.status = new_status

        if new_status == OrderStatusType.COMPLETED:
            order.completed_at = datetime.now(timezone.utc)

        self.session.add(
            OrderHistoryStatus(
                order_id=order_id,
                old_status=old_status,
                new_status=new_status,
                changed_by=changed_by
            )
        )

        await self.session.flush()