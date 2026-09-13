from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Employees, UserRole, Users


class EmployeeRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_employees_by_company_id(self, company_id: int):
        result = await self.session.execute(
            select(Employees).where(Employees.company_id == company_id)
        )

    async def get_employee_by_id(self, employee_id: int) -> Employees | None:
        result = await self.session.execute(
            select(Employees).where(Employees.id == employee_id)
        )

        return result.scalar_one_or_none()

    async def delete_employee(self, employee_id: int):
        await self.session.execute(
            delete(Employees)
            .where(Employees.id == employee_id)
        )

    async def update_employee_role(self, new_role: UserRole, user_id: int):
        await self.session.execute(
            update(Users)
            .values(role=new_role)
            .where(Users.id == user_id)
        )