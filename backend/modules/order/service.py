from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import OrderStatusType, StatusType
from database.models import CompanyMembers, Orders, MembersRole
from modules.order.repo import OrderRepo
from modules.order.schema import OrderParams
from modules.order.policies import (
    ALLOWED_TRANSITIONS,
    WORKER_TARGET_STATUSES,
)
from utils.logger import logger


class OrderService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = OrderRepo(session)

    async def get_order_history(self, order: Orders, member: CompanyMembers):
        if member.company_id != order.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company id not match"
            )

        order_history = await self.repo.get_history(order.id)
        return order_history

    async def get_orders(self, member: CompanyMembers):
        orders = await self.repo.get_orders(member.company_id)
        return orders

    async def create_order(self, params: OrderParams, member: CompanyMembers):
        service = await self.repo.get_service_by_id(params.service_id)
        if service is None:
            logger.exception("Failed to create order comapny_id={}", member.company_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        if service.company_id != member.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company and member do not match"
            )

        try:
            order_id = await self.repo.create_order(params, member)
            await self.db.commit()

            return {
                "order_id": order_id,
                "message": "New order created successfully",
            }

        except Exception:
            await self.db.rollback()

            logger.exception("Failed to create order {}")

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create order"
            )

    async def get_order_by_id(self, order: Orders, member: CompanyMembers):
        if order.company_id != member.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company and member do not match"
                )

        return order

    async def update_order_status(self, order_id: int, member: CompanyMembers, new_status: OrderStatusType):
        try:
            order = await self.repo.get_for_update(order_id, member.company_id)

            if order is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Order not found"
                )

            if member.status != StatusType.ACTIVE:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Company and member do not match"
                )

            if member.role == MembersRole.WORKER:
                if order.assigned_employee_id != member.id:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Order is not assigned to you"
                    )

                if new_status not in WORKER_TARGET_STATUSES:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient permissions"
                    )

            if new_status not in ALLOWED_TRANSITIONS[order.status]:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Transition {order.status.value} -> "
                    f"{new_status.value} is not allowed",
                )

            if new_status == OrderStatusType.ASSIGNED:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Use the employee assignment operation"
                )

            await self.repo.change_status(
                order.id,
                order,
                new_status,
                changed_by=member.user_id
            )

            await self.db.commit()

            return {
                "order_id": order.id,
                "new_status": new_status,
            }

        except Exception:
            await self.db.rollback()
            raise

    async def assigned_employee(self, order: Orders, assigned_employee_id: int, member: CompanyMembers):
        if order.company_id != member.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company and member do not match"
            )

        employee = await self.repo.get_employee_by_id(assigned_employee_id)
        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee not found"
            )

        if employee.company_id != member.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Company and member do not match"
            )

        if employee.status != StatusType.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee is inactive"
            )

        try:
            await self.repo.assigned_employee(order.id, assigned_employee_id)
            await self.repo.change_status(
                order.id,
                order,
                OrderStatusType.ASSIGNED,
                changed_by=member.user_id
            )

            await self.db.commit()

            return {
                "employee_id": assigned_employee_id,
                "message": f"{employee.first_name} {employee.last_name} a task was assigned",
            }

        except Exception:
            await self.db.rollback()
            raise