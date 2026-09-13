from fastapi import APIRouter, Depends

from app.database.models import Users, Employees
from app.modules.auth.deps import check_owner_user
from app.modules.employees.deps import get_employee_service, check_employee_id
from app.modules.employees.schema import NewUserParams
from app.modules.employees.service import EmployeeService


router = APIRouter(tags=["Employee"], prefix="/employees")


@router.get("/")
async def get_employees(
        current_owner: Users = Depends(check_owner_user),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.get_employees(current_owner)


@router.get("/{employee_id}")
async def get_employee(
        employee: Employees = Depends(check_employee_id),
        current_owner: Users = Depends(check_owner_user),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.get_employee(employee, current_owner)


@router.patch("/{employee_id}")
async def update_employee(
        params: NewUserParams,
        employee: Employees = Depends(check_employee_id),
        current_owner: Users = Depends(check_owner_user),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.patch_employee(params, employee, current_owner)


@router.delete("/{employee_id}")
async def delete_employee(
        employee: Employees = Depends(check_employee_id),
        current_owner: Users = Depends(check_owner_user),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.delete_employee(employee, current_owner)