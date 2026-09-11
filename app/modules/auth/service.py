from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.repository import AuthRepo
from app.modules.auth.schemas import RegisterCompanySchema


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repo = AuthRepo(session)

    async def register_new_company(self, params: RegisterCompanySchema):
        exists_company = await self.repo.get_company_by_phone_or_email(params.email, params.phone)

        for company in exists_company:
            if company.email == params.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            if company.phone == params.phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone already registered"
                )

        company_id = await self.repo.create_company(params)

        return {
            'id': company_id,
            "message": "Company created",
        }