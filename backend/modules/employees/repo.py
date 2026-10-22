from typing import List

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import StatusType
from database.models import CompanyMembers
from modules.employees.schema import NewUserParams


class EmployeeRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_employees_by_company_id(self, company_id: int) -> List[CompanyMembers]:
        result = await self.session.execute(
            select(CompanyMembers)
            .where(CompanyMembers.company_id == company_id)
        )

        return result.scalars().all()

    async def get_employee_by_id(self, employee_id: int) -> CompanyMembers | None:
        result = await self.session.execute(
            select(CompanyMembers).where(CompanyMembers.id == employee_id)
        )

        return result.scalar_one_or_none()

    async def delete_employee(self, employee_id: int):
        await self.session.execute(
            update(CompanyMembers)
            .where(CompanyMembers.id == employee_id)
            .values(status=StatusType.INACTIVE)
        )

    async def update_employee(self, params: NewUserParams, user_id: int):
        update_data = params.model_dump(exclude_unset=True, exclude_none=True)
        await self.session.execute(
            update(CompanyMembers)
            .where(CompanyMembers.user_id == user_id)
            .values(**update_data)
        )
