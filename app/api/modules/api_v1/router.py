from fastapi import APIRouter, Depends

from app.api.modules.api_v1.deps import get_company_service, check_exists_company_id
from app.api.modules.api_v1.schemas import NewCompanySchema
from app.api.modules.api_v1.service import CompanyService
from app.database.models import Companies


router = APIRouter()


@router.post("/api/v1/companies")
async def create_company(
        params: NewCompanySchema,
        service: CompanyService = Depends(get_company_service)
):
    return await service.create_company(params)


@router.get("/api/v1/companies/{company_id}")
async def get_company(
        company: Companies = Depends(check_exists_company_id),
        service: CompanyService = Depends(get_company_service)
):
    return await service.get_company(company.id)


@router.patch("/api/v1/companies/{company_id}")
async def update_company(
        params: NewCompanySchema,
        company: Companies = Depends(check_exists_company_id),
        service: CompanyService = Depends(get_company_service)
):
    return await service.update_company(company.id, params)


@router.delete("/api/v1/companies/{company_id}")
async def delete_company(
        company: Companies = Depends(check_exists_company_id),
        service: CompanyService = Depends(get_company_service)
):
    return await service.delete_company(company.id)