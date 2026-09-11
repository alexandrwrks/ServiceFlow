from typing import List

from sqlalchemy import or_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Companies, Users, UserRole, Employees
from app.modules.auth.schemas import RegisterCompanySchema, RegisterUserSchema


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
            .values(
                name=params.name,
                description=(params.description if params.description else None),
                phone=(params.phone if params.phone else None),
                email=params.email,
            )
            .returning(Companies.id)
        )

        return result.scalar_one()

    async def register_owner_to_company(self, company_id: int, params: RegisterUserSchema, password_hash: str):
        result = await self.session.execute(
            insert(Users)
            .values(
                company_id=company_id,
                email=params.email,
                password_hash=password_hash,
                role=UserRole.OWNER
            )
            .returning(Users.id)
        )

        await self.session.flush()

        user_id = result.scalar_one()

        await self.session.execute(
            insert(Employees)
            .values(
                company_id=company_id,
                user_id=user_id,
                first_name=params.first_name,
                last_name=params.last_name,
            )
        )

    async def get_user_by_email(self, email: str) -> Users | None:
        result = await self.session.execute(
            select(Users)
            .where(Users.email == email)
        )

        return result.scalar_one_or_none()