from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Users, UserRole, StatusType
from app.jwt.schemas import TokenData
from app.jwt.service import jwt_service
from app.modules.auth.repository import AuthRepo
from app.modules.auth.schemas import RegisterCompanyRequest, InvitationSchema, LoginUserSchema
from app.utils.security.password import hashed_password, verify_password
from app.utils.security.token import hashed_token, create_invitation_token, verify_token


class AuthService:
    def __init__(self, session: AsyncSession):
        self.db = session
        self.repo = AuthRepo(session)

    async def register_company(self, params: RegisterCompanyRequest):
        password_hash = hashed_password(params.owner.password)

        try:
            async with self.db.begin():
                exists_company = await self.repo.get_company_by_phone_or_email(
                    params.company.email,
                    params.company.phone
                )

                for company in exists_company:
                    if company.email == params.company.email:
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="Email already registered"
                        )

                    if company.phone == params.company.phone:
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="Phone already registered"
                        )

                exist_user = await self.repo.get_user_by_email(params.owner.email)
                if exist_user:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email already registered"
                    )

                company_id = await self.repo.create_company(params.company)

                await self.repo.register_owner_to_company(company_id, params.owner, password_hash)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company or owner already exists"
            )

        return {
            "company_id": company_id,
            "message": "Company created",
        }

    async def check_user(self, access_token: str) -> Users:
        payload = jwt_service.verify_access_token(access_token)
        user_id = int(payload.get('sub'))

        exists_user = await self.repo.get_user_by_id(user_id)
        if exists_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return exists_user

    async def check_owner_user(self, user: Users) -> Users:
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
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        password_hash = hashed_password(params.password)
        token, token_hash, expired_at = create_invitation_token()

        try:
            user_id = await self.repo.create_employee(params, user.company_id, password_hash)
            await self.repo.add_employee_token(user_id, token_hash, expired_at)

            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee already exists"
            )

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

        try:
            await self.repo.update_user_password(user_id, password_hash)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to update user"
            )

        return {
            "message": "Employee activated",
        }

    async def login(self, params: LoginUserSchema):
        exist_user = await self.repo.get_user_by_email(params.email)
        if exist_user is None or not verify_password(exist_user.password_hash, params.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if exist_user.status == StatusType.INACTIVE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )

        tokens = jwt_service.get_tokens(
            TokenData(
                user_id=exist_user.id,
                role=exist_user.role,
                company_id=exist_user.company_id,
            )
        )

        refresh_token_hash = hashed_token(tokens.refresh_token)

        try:
            await self.repo.insert_token(refresh_token_hash, exist_user.id)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed login"
            )

        return tokens

    async def logout(self, user_id: int):
        try:
            await self.repo.inactive_token(user_id)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ошибка обновления данных"
            )

        return {
            "user_id": user_id,
            "message": "User logged out",
        }


    async def refresh(self, refresh_token: str, user: Users):
        token_hash = await self.repo.get_refresh_token_by_user_id(user.id)
        if token_hash is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Refresh token not found"
            )

        token_verify = verify_token(
            hash_token=token_hash.hash_refresh_token,
            token=refresh_token,
        )

        if not token_verify:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        tokens = jwt_service.get_tokens(
            TokenData(
                user_id=user.id,
                role=user.role,
                company_id=user.company_id,
            )
        )

        refresh_token_hash = hashed_token(tokens.refresh_token)

        try:
            await self.repo.delete_token(user.id)
            await self.repo.insert_token(refresh_token_hash, user.id)
            await self.db.commit()

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Failed to update refresh token"
            )

        return tokens