from fastapi import APIRouter, Depends

from database.enum import MembersRole
from database.models import CompanyMembers
from modules.employees.deps import get_employee_service, check_employee_id, check_roles_without_company_id, \
    EmployeeExists
from modules.employees.schema import NewUserParams
from modules.employees.service import EmployeeService


router = APIRouter(tags=["Employee"], prefix="/employees")


@router.get("/")
async def get_employees(
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER
            ),
        ),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.get_employees(current_member)


@router.get("/{employee_id}")
async def get_employee(
        employee: EmployeeExists,
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER
            ),
        ),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.get_employee(employee, current_member)


@router.patch("/{employee_id}")
async def update_employee(
        params: NewUserParams,
        employee: EmployeeExists,
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER
            ),
        ),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.patch_employee(employee, current_member, params)


@router.delete("/{employee_id}")
async def delete_employee(
        employee: EmployeeExists,
        current_member: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER
            ),
        ),
        service: EmployeeService = Depends(get_employee_service)
):
    return await service.delete_employee(employee, current_member)