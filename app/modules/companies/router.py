from fastapi import APIRouter, Depends

from app.modules.companies.deps import get_company_service, check_exists_company_id
from app.modules.companies.schemas import NewCompanySchema
from app.modules.companies.service import CompanyService
from app.database.models import Companies


router = APIRouter()


@router.post("/")
async def create_company(
    params: NewCompanySchema, service: CompanyService = Depends(get_company_service)
):
    return await service.create_company(params)


@router.get("/{company_id}")
async def get_company(
    company: Companies = Depends(check_exists_company_id),
    service: CompanyService = Depends(get_company_service),
):
    return await service.get_company(company.id)


@router.patch("/{company_id}")
async def update_company(
    params: NewCompanySchema,
    company: Companies = Depends(check_exists_company_id),
    service: CompanyService = Depends(get_company_service),
):
    return await service.update_company(company.id, params)


@router.delete("/{company_id}")
async def delete_company(
    company: Companies = Depends(check_exists_company_id),
    service: CompanyService = Depends(get_company_service),
):
    return await service.delete_company(company.id)
