from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import MembersRole
from database.models import Companies, Users, CompanyMembers
from modules.companies.repo import CompanyRepo
from modules.companies.schemas import ResponseCompany, CreateCompanyRequest, UpdateCompanySchema
from cache.cache_service import CacheService
from utils.logger import logger


class CompanyService:
    def __init__(self, session: AsyncSession, cache: CacheService):
        self.db = session
        self.cache = cache
        self.repo = CompanyRepo(session)

    async def get_company(self, company: Companies) -> ResponseCompany:
        key = f"company:{company.id}"

        cached = await self.cache.get(key, ResponseCompany)
        if cached is not None:
            logger.info("REDIS HIT: {}", key)
            return cached

        logger.info("REDIS MISS: {}", key)

        response = ResponseCompany.model_validate(company)
        await self.cache.set(key, response)

        return response

    async def delete_company(self, member: CompanyMembers):
        key = f"company:{member.company_id}"

        try:
            count_of_members = await self.repo.delete_company(member.company_id)

            await self.cache.delete(key)

            await self.db.commit()

            logger.info("Successfully delete company: {}", member.company_id)

            return {
                "id": member.company_id,
                "count_of_members": count_of_members,
                "message": "The company has become inactive",
            }

        except Exception:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to delete company",
            )

    async def create_company(self, user: Users, params: CreateCompanyRequest):
        try:
            company_id = await self.repo.create_company(user.id, params.company)

            await self.repo.create_owner_member(
                company_id=company_id,
                user_id=user.id,
                params=params.owner
            )
            await self.db.commit()

            logger.info("Successfully create company: {}", company_id)
            return {
                "company_id": company_id,
                "user_id": user.id,
                "role": MembersRole.OWNER,
                "message": "Company created successfully",
            }

        except IntegrityError:
            await self.db.rollback()
            logger.exception("Failed to create company")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to create company",
            )

    async def update_company(self, member: CompanyMembers, params: UpdateCompanySchema):
        key = f"company:{member.company_id}"
        try:
            await self.repo.update_company(member.company_id, params)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to update company",
            )

        except Exception:
            await self.db.rollback()

            logger.exception("Failed to update company")
            raise

        await self.cache.delete(key)
        return {
            "company_id": member.company_id,
            "message": "Company updated successfully",
        }
