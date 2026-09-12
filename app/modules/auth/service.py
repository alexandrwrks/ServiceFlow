import uuid
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users, UserRole
from app.jwt.service import jwt_service
from app.modules.auth.repository import AuthRepo
from app.modules.auth.schemas import RegisterCompanyRequest, InvitationSchema
from app.utils.security.password import hashed_password
from app.utils.security.token import hashed_token

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

    async def check_user(self, access_token: str) -> Users:
        payload = jwt_service.verify_refresh_token(access_token)
        user_id = int(payload.get('sub'))

        exists_user = await self.repo.get_user_by_id(user_id)
        if exists_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return exists_user

    async def check_owner_user(self, user: Users):
        if user.role != UserRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not owner"
            )

        return user

    async def register_new_employee(self, params: InvitationSchema, user: Users):
        exist_user = await self.repo.get_user_by_email(params.email)
        if exist_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        password_hash = hashed_password(params.password)

        user_id = await self.repo.create_employee(params, user.company_id, password_hash)

        token = uuid.uuid4().hex
        token_hash = hashed_token(token)
        expired_at = datetime.now(timezone.utc) + timedelta(days=3)

        await self.repo.add_employee_token(user_id, token_hash, expired_at)

        return {
            "token": f"/employees/invitations/{token}/activate",
            "message": "Employee created",
        }

    async def accept_employee_invitation(self, token: str, new_password: str):
        token_hash = hashed_token(token)

        user_id = await self.repo.get_employee_id_by_token(token_hash)

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )

        password_hash = hashed_password(new_password)
        
        await self.repo.update_user_password(user_id, password_hash)

        return {
            "message": "Employee activated",
        }