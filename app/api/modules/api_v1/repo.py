from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.modules.api_v1.schemas import NewCompanySchema
from app.database.models import Companies


class CompanyRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_company_by_id(self, company_id: int) -> Companies | None:
        result = await self.db.execute(
            select(Companies)
            .where(Companies.id == company_id)
        )

        return result.scalar_one_or_none()

    async def delete_company(self, company_id: int) -> None:
        await self.db.execute(
            delete(Companies)
            .where(Companies.id == company_id)
        )

    async def create_company(self, params: NewCompanySchema) -> int:
        result = await self.db.execute(
            insert(Companies)
            .values(
                name=params.title,
                description=params.description,
                phone=params.phone,
                email=params.email,
            )
            .returning(Companies.id)
        )

        return result.scalar_one()

    async def update_company(self, company_id: int, params: NewCompanySchema):
        await self.db.execute(
            update(Companies)
            .where(Companies.id == company_id)
            .values(
                name=params.title,
                description=params.description,
                phone=params.phone,
                email=params.email,
            )
        )