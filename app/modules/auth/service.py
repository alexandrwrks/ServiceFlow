from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.repository import AuthRepo
from app.modules.auth.schemas import RegisterCompanySchema, RegisterUserSchema, RegisterCompanyRequest
from app.utils.security.password import hashed_password


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = AuthRepo(session)

    async def register_company(self, params: RegisterCompanyRequest):
        exists_company = await self.repo.get_company_by_phone_or_email(params.company.email, params.company.phone)
        for company in exists_company:
            if company.email == params.company.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            if company.phone == params.company.phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone already registered"
                )

        exist_user = await self.repo.get_user_by_email(params.owner.email)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        password_hash = hashed_password(params.owner.password)
        company_id = await self.repo.create_company(params.company)

        await self.repo.register_owner_to_company(company_id, params.owner, password_hash)

        return {
            "company_id": company_id,
            "message": "Company created",
        }