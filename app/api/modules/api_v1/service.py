from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.modules.api_v1.repo import CompanyRepo
from app.api.modules.api_v1.schemas import NewCompanySchema


class CompanyService:
    def __init__(self, session: AsyncSession):
        self.repo = CompanyRepo(session)

    async def get_company(self, company_id: int):
        company = await self.repo.get_company_by_id(company_id)
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        return company

    async def delete_company(self, company_id: int):
        await self.repo.delete_company(company_id)

        return {
            "id": company_id,
            "message": "Company deleted successfully",
        }

    async def create_company(self, params: NewCompanySchema):
        company_id = await self.repo.create_company(params)

        return {
            "id": company_id,
            "message": "Company created successfully",
        }

    async def update_company(self, company_id: int, params: NewCompanySchema):
        await self.repo.update_company(company_id, params)

        return {
            "id": company_id,
            "message": "Company updated successfully",
        }