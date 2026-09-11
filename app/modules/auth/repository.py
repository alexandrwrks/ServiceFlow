from typing import List

from sqlalchemy import or_, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Companies
from app.modules.auth.schemas import RegisterCompanySchema


class AuthRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_company_by_phone_or_email(self, email: str, phone: str | None = None) -> List[Companies]:
        if phone is not None:
            query = select(Companies).where(
                or_(
                    Companies.email == email,
                    Companies.phone == phone
                )
            )
        else:
            query = select(Companies).where(Companies.email == email)

        result = await self.session.execute(query)

        return result.scalars().all()

    async def create_company(self, params: RegisterCompanySchema) -> int:
        result = await self.session.execute(
            insert(Companies)
            .values(*params)
            .returning(Companies.id)
        )

        return result.scalar_one()