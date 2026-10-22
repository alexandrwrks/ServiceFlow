from datetime import datetime, timezone, timedelta
from typing import List

from sqlalchemy import or_, select, update, func, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.enum import KeyStatusType
from database.models import Companies, Users, CompanyMembers, UsersToken, RefreshTokens
from modules.auth.schemas import RegisterCompanySchema, RegisterUserSchema, InvitationSchema
from utils.settings import settings


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

    async def get_employee_by_id(self, user_id: int) -> CompanyMembers | None:
        result = await self.session.execute(
            select(CompanyMembers)
            .where(CompanyMembers.user_id == user_id)
        )

        return result.scalar_one_or_none()

    async def create_employee(
            self, params: InvitationSchema, company_id: int, password_hash: str
    ) -> int:
        user_result = await self.session.execute(
            insert(Users)
            .values(
                email=params.email,
                password_hash=password_hash,
            )
            .returning(Users.id)
        )

        await self.session.flush()

        user_id = user_result.scalar_one()

        await self.session.execute(
            insert(CompanyMembers)
            .values(
                company_id=company_id,
                user_id=user_id,
                role=params.role,
                first_name=params.first_name,
                last_name=params.last_name,
                phone=(params.phone if params.phone else None),
            )
        )

        return user_id

    async def add_employee_token(self, user_id: int, token_hash: str, expired_at: datetime):
        await self.session.execute(
            insert(UsersToken)
            .values(
                user_id=user_id,
                token_hash=token_hash,
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
                UsersToken.expired_at > func.now()
            )
        )

    async def get_refresh_token_by_user_id(self, user_id: int) -> RefreshTokens | None:
        result = await self.session.execute(
            select(RefreshTokens)
            .where(
                RefreshTokens.user_id == user_id,
                RefreshTokens.expired_at > datetime.now(timezone.utc),
                RefreshTokens.status.is_(KeyStatusType.ACTIVE)
            )
        )

        return result.scalar_one_or_none()

    async def inactive_token(self, user_id: int):
        await self.session.execute(
            update(RefreshTokens)
            .values(status=KeyStatusType.REVOKED)
            .where(RefreshTokens.user_id == user_id)
        )

    async def insert_token(self, new_token: str, user_id: int):
        await self.session.execute(
            insert(RefreshTokens)
            .values(
                user_id=user_id,
                hash_refresh_token=new_token,
                expired_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_DAYS)
            )
        )

    async def delete_token(self, user_id: int):
        await self.session.execute(
            delete(RefreshTokens)
            .where(RefreshTokens.user_id == user_id)
        )

    async def register_new_user(self, params: RegisterUserSchema) -> int:
        result = await self.session.execute(
            insert(Users)
            .values(
                email=params.email,
                password_hash=params.password,
            )
            .returning(Users.id)
        )

        return result.scalar_one()

    async def get_member_by_user(self, user: Users) -> CompanyMembers | None:
        result = await self.session.execute(
            select(CompanyMembers)
            .where(CompanyMembers.user_id == user.id)
        )

        return result.scalar_one_or_none()