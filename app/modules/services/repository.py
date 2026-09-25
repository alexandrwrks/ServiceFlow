from typing import List

from sqlalchemy import select, update, not_, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Services, Users
from app.modules.services.schema import CreateNewService, UpdateService


class ProviderRepo:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_company_service_by_id(self, company_id: int) -> List[Services]:
        result = await self.db.execute(
            select(Services)
            .where(Services.company_id == company_id)
        )

        return result.scalars().all()

    async def create_company_service(self, params: CreateNewService, employee: Users) -> int:
        result = await self.db.execute(
            insert(Services)
            .values(
                company_id=employee.company_id,
                name=params.name,
                description=params.description,
                base_price=params.base_price,
                duration_minutes=(params.duration_minutes if params.duration_minutes else None),
            )
            .returning(Services.id)
        )

        return result.scalar_one()

    async def get_service_by_id(self, service_id: int) -> Services | None:
        result = await self.db.execute(
            select(Services)
            .where(Services.id == service_id)
        )

        return result.scalar_one_or_none()

    async def update_company_service(self, service_id: int, params: UpdateService):
        await self.db.execute(
            update(Services)
            .where(Services.id == service_id)
            .values(**params.model_dump(exclude_none=True))
        )

    async def patch_company_service_status(self, service_id: int):
        await self.db.execute(
            update(Services)
            .where(Services.id == service_id)
            .values(is_active=not_(Services.is_active))
        )

    async def delete_company_service(self, service_id: int):
        await self.db.execute(
            delete(Services)
            .where(Services.id == service_id)
        )