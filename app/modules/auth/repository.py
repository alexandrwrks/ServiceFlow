from datetime import datetime, timezone
from typing import List

from sqlalchemy import or_, select, and_, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Companies, Users, UserRole, Employees, UsersToken
from app.modules.auth.schemas import RegisterCompanySchema, RegisterUserSchema, InvitationSchema


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

    async def get_user_by_id(self, user_id: int) -> Users | None:
        result = await self.session.execute(
            select(Users)
            .where(Users.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_employee_by_id(self, user_id: int) -> Employees | None:
        result = await self.session.execute(
            select(Employees)
            .where(Employees.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def create_employee(
            self, params: InvitationSchema, company_id: int, password_hash: str
    ) -> int:
        user_result = await self.session.execute(
            insert(Users)
            .values(
                company_id=company_id,
                email=params.email,
                password_hash=password_hash,
                role=params.role,
            )
            .returning(Users.id)
        )

        await self.session.flush()

        user_id = user_result.scalar_one()

        await self.session.execute(
            insert(Employees)
            .values(
                company_id=company_id,
                user_id=user_id,
                first_name=params.first_name,
                last_name=params.last_name,
                phone=(params.phone if params.phone else None),
            )
        )

        return user_id

    async def add_employee_token(self, user_id: int, token: str, expired_at: datetime):
        await self.session.execute(
            insert(UsersToken)
            .values(
                user_id=user_id,
                token=token,
                expired_at=expired_at
            )
        )

    async def get_employee_id_by_token(self, token_hash: str) -> int | None:
        result = await self.session.execute(
            select(UsersToken.user_id)
            .where(
                UsersToken.token_hash == token_hash,
                UsersToken.used.is_(False),
                UsersToken.expired_at > datetime.now(timezone.utc)
            )
        )

        return result.scalar_one_or_none()

    async def update_user_password(self, user_id: int, new_password_hash: str):
        await self.session.execute(
            update(Users)
            .values(password_hash=new_password_hash)
            .where(Users.id == user_id)
        )

        await self.session.execute(
            update(UsersToken)
            .values(used=True)
            .where(
                UsersToken.user_id == user_id,
                UsersToken.expired_at.is_(False)
            )
        )