from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users, Employees
from app.modules.employees.repo import EmployeeRepo
from app.modules.employees.schema import NewUserParams


class EmployeeService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = EmployeeRepo(session)

    async def get_employees(self, owner: Users):
        return await self.repo.get_employees_by_company_id(owner.company_id)

    async def get_employee(self, employee: Employees, owner: Users):
        if employee.company_id != owner.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недоступно"
            )

        return employee

    async def delete_employee(self, employee: Employees, owner: Users):
        if employee.company_id != owner.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недоступно"
            )

        try:
            await self.repo.delete_employee(employee.id)
            await self.db.commit()

        except SQLAlchemyError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to delete employee"
            )

    async def patch_employee(self, params: NewUserParams, employee: Employees, owner: Users):
        if employee.company_id != owner.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недоступно"
            )

        if params.new_role is not None:
            try:
                await self.repo.update_employee_role(params.new_role, employee.user_id)
                await self.db.commit()
            except IntegrityError:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Failed to update employee role"
                )

        return {
            "id": employee.id,
            "message": "Employee updated successfully"
        }