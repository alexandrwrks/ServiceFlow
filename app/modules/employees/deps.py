from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import get_async_session
from app.database.models import Employees
from app.modules.employees.repo import EmployeeRepo
from app.modules.employees.service import EmployeeService


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
) -> Employees:
    exist_employee = await repo.get_employee_by_id(employee_id)
    if exist_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} not found",
        )

    return exist_employee