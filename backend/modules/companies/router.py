from fastapi import APIRouter, Depends

from database.enum import MembersRole
from dependencies_factory import check_roles
from modules.auth.deps import get_current_user
from modules.companies.deps import get_company_service, CompanyExists
from modules.companies.schemas import CreateCompanyRequest, UpdateCompanySchema
from modules.companies.service import CompanyService
from database.models import Users, CompanyMembers


router = APIRouter()


@router.post("/")
async def create_company(
    params: CreateCompanyRequest,
    current_user: Users = Depends(get_current_user),
    service: CompanyService = Depends(get_company_service)
):
    return await service.create_company(current_user, params)


@router.get("/{company_id}")
async def get_company(
    company: CompanyExists,
    service: CompanyService = Depends(get_company_service),
):
    return await service.get_company(company)


@router.patch("/{company_id}")
async def update_company(
    params: UpdateCompanySchema,
    current_member: CompanyMembers = Depends(
        check_roles(
            MembersRole.OWNER
        )
    ),
    service: CompanyService = Depends(get_company_service),
):
    return await service.update_company(current_member, params)


@router.delete("/{company_id}")
async def delete_company(
    current_member: CompanyMembers = Depends(
        check_roles(
            MembersRole.OWNER
        )
    ),
    service: CompanyService = Depends(get_company_service),
):
    return await service.delete_company(current_member)
