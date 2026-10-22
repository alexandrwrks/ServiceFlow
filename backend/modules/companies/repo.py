from sqlalchemy import select, delete, update, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import MembersRole, StatusType
from modules.companies.schemas import NewCompanySchema, OwnerProfileSchema, UpdateCompanySchema
from database.models import Companies, CompanyMembers


class CompanyRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_company_by_id(self, company_id: int) -> Companies | None:
        result = await self.db.execute(
            select(Companies).where(Companies.id == company_id)
        )

        return result.scalar_one_or_none()

    async def delete_company(self, company_id: int) -> int:
        await self.db.execute(
            update(Companies)
            .where(Companies.id == company_id)
            .values(active=StatusType.INACTIVE)
        )

        result = await self.db.execute(
            update(CompanyMembers)
            .where(CompanyMembers.company_id == company_id)
            .values(status=StatusType.INACTIVE)
            .returning(CompanyMembers.id)
        )

        return len(result.scalars().all())

    async def create_company(self, user_id: int, params: NewCompanySchema) -> int:
        result = await self.db.execute(
            insert(Companies)
            .values(
                name=params.name,
                description=params.description,
                phone=params.phone,
                email=params.email,
                user_id=user_id
            )
            .returning(Companies.id)
        )

        return result.scalar_one()

    async def update_company(self, company_id: int, params: UpdateCompanySchema):
        update_data = params.model_dump(exclude_none=True, exclude_unset=True)
        await self.db.execute(
            update(Companies)
            .where(Companies.id == company_id)
            .values(**update_data)
        )

    async def get_company_member(self, company_id: int, user_id: int) -> CompanyMembers | None:
        result = await self.db.execute(
            select(CompanyMembers)
            .where(
                CompanyMembers.company_id == company_id,
                CompanyMembers.user_id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def create_owner_member(self, company_id: int, user_id: int, params: OwnerProfileSchema):
        await self.db.execute(
            insert(CompanyMembers)
            .values(
                company_id=company_id,
                user_id=user_id,
                role=MembersRole.OWNER,
                first_name=params.first_name,
                last_name=params.last_name,
                phone=params.phone,
            )
        )
