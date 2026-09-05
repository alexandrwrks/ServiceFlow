from fastapi import APIRouter, Depends

from app.api.modules.api_v1.deps import get_company_service
from app.api.modules.api_v1.schemas import NewCompanySchema
from app.api.modules.api_v1.service import CompanyService

router = APIRouter()


@router.post("/api/v1/companies")
async def create_company(
        params: NewCompanySchema = Depends(),
        service: CompanyService = Depends(get_company_service)
):
    return await service.create_company(params)

@router.get("/api/v1/companies/{company_id}")
async def get_company(
        company_id: int,
        service: CompanyService = Depends(get_company_service)
):
    return await service.get_company(company_id)

@router.patch("/api/v1/companies/{company_id}")
async def update_company(
        company_id: int,
        params: NewCompanySchema = Depends(),
        service: CompanyService = Depends(get_company_service)
):
    return await service.update_company(company_id, params)

@router.delete("/api/v1/companies/{company_id}")
async def delete_company(
        company_id: int,
        service: CompanyService = Depends(get_company_service)
):
    return await service.delete_company(company_id)