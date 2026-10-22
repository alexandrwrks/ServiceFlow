from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import MembersRole, EMPLOYEES_ROLES
from database.models import CompanyMembers
from modules.employees.repo import EmployeeRepo
from modules.employees.schema import NewUserParams


class EmployeeService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = EmployeeRepo(session)

    async def get_employees(self, current_member: CompanyMembers):
        employees = await self.repo.get_employees_by_company_id(current_member.company_id)

        return employees

    async def get_employee(self, employee: CompanyMembers, current_member: CompanyMembers):
        if employee.company_id != current_member.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недоступно"
            )

        return employee

    async def delete_employee(self, employee: CompanyMembers, current_member: CompanyMembers):
        if employee.company_id != current_member.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недоступно"
            )

        if employee.role == MembersRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Сначала передайте владение компанией другому сотруднику",
            )

        if employee.role == MembersRole.ADMIN and current_member.role != MembersRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You don't have permission to perform this action"
            )

        if current_member.role == MembersRole.MANAGER and employee.role != MembersRole.WORKER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action"
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

    async def patch_employee(self, employee: CompanyMembers, current_member: CompanyMembers, params: NewUserParams):
        if employee.company_id != current_member.company_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недоступно"
            )

        if employee.role == MembersRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Сначала передайте владение компанией другому сотруднику",
            )

        if (employee.role == MembersRole.OWNER or employee.role == MembersRole.ADMIN) and current_member.role in EMPLOYEES_ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action"
            )

        if employee.id == current_member.id and current_member.role in EMPLOYEES_ROLES:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action"
            )

        if current_member.role == MembersRole.MANAGER and params.role == MembersRole.WORKER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action"
            )

        if params.role is not None:
            try:
                await self.repo.update_employee(params, employee.user_id)
                await self.db.commit()

                return {
                    "id": employee.id,
                    "message": "Employee updated successfully"
                }

            except IntegrityError:
                await self.db.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Failed to update employee role"
                )