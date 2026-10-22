from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import get_async_session
from database.enum import MembersRole, StatusType
from database.models import CompanyMembers
from modules.auth.deps import get_current_member
from modules.employees.repo import EmployeeRepo
from modules.employees.service import EmployeeService


async def get_employee_service(
        session: AsyncSession = Depends(get_async_session),
):
    return EmployeeService(session)

async def get_employee_repo(
        session: AsyncSession = Depends(get_async_session),
):
    return EmployeeRepo(session)

async def check_employee_id(
        employee_id: int,
        repo: EmployeeRepo = Depends(get_employee_repo)
) -> CompanyMembers:
    exist_employee = await repo.get_employee_by_id(employee_id)
    if exist_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found",
        )

    return exist_employee

EmployeeExists = Annotated[CompanyMembers, Depends(check_employee_id)]

def check_roles_without_company_id(*allowed_roles: MembersRole):
    async def role_checker(
        member: CompanyMembers = Depends(get_current_member),
    ) -> CompanyMembers:
        if member.status == StatusType.INACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Сотрудник не активен",
            )

        if member.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав",
            )

        return member

    return role_checker