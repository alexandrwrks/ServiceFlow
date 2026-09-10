from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.companies.repo import CompanyRepo
from app.modules.companies.schemas import NewCompanySchema, ResponseCompany
from app.cache.cache_service import CacheService
from app.utils.logger import logger


class CompanyService:
    def __init__(self, session: AsyncSession, cache: CacheService):
        self.repo = CompanyRepo(session)
        self.cache = cache

    async def get_company(self, company_id: int) -> ResponseCompany:
        key = f"company:{company_id}"

        cached = await self.cache.get(key, ResponseCompany)
        if cached is not None:
            logger.info("REDIS HIT: {}", key)
            return cached

        logger.info("REDIS MISS: {}", key)
        company = await self.repo.get_company_by_id(company_id)
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        response = ResponseCompany.model_validate(company)
        await self.cache.set(key, response)

        return response

    async def delete_company(self, company_id: int):
        key = f"company:{company_id}"
        await self.repo.delete_company(company_id)

        await self.cache.delete(key)

        logger.info("Successfully delete company: {}", company_id)
        return {
            "id": company_id,
            "message": "Company deleted successfully",
        }

    async def create_company(self, params: NewCompanySchema):
        try:
            company_id = await self.repo.create_company(params)
        except Exception:
            logger.exception("Failed to create company")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_ERROR,
                detail="Failed to create company",
            )

        logger.info("Successfully create company: {}", company_id)
        return {
            "id": company_id,
            "message": "Company created successfully",
        }

    async def update_company(self, company_id: int, params: NewCompanySchema):
        key = f"company:{company_id}"
        try:
            await self.repo.update_company(company_id, params)
        except Exception:
            logger.exception("Failed to update company")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_ERROR,
                detail="Failed to update company",
            )

        await self.cache.delete(key)
        return {
            "id": company_id,
            "message": "Company updated successfully",
        }
