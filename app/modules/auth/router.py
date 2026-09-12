from fastapi import APIRouter, Depends

from app.database.models import Users
from app.modules.auth.deps import get_auth_service, check_owner_user, get_current_user
from app.modules.auth.schemas import LoginUserSchema, RegisterCompanyRequest, InvitationSchema, NewPasswordSchema
from app.modules.auth.service import AuthService

router = APIRouter()


@router.post("/telegram")
async def telegram_auth(
        service: AuthService = Depends(get_auth_service)
):
    return await service.telegram_auth()


@router.post("/register-company")
async def register_user(
        params: RegisterCompanyRequest,
        service: AuthService = Depends(get_auth_service)
):
    return await service.register_company(params)


@router.post("/employees/invitations")
async def register_employee(
        params: InvitationSchema,
        owner_user: Users = Depends(check_owner_user),
        service: AuthService = Depends(get_auth_service)
):
    return await service.register_new_employee(params, owner_user)


@router.post("/employees/invitations/{token}/activate")
async def activate_employee(
        token: str,
        params: NewPasswordSchema,
        service: AuthService = Depends(get_auth_service)
):
    """Активация сотрудника"""
    return await service.accept_employee_invitation(token, params.new_password)


@router.post("/login")
async def login_user(
        params: LoginUserSchema,
        service: AuthService = Depends(get_auth_service)
):
    return await service.login(params)


@router.post("/logout")
async def logout_user(
        refresh_token: str,
        current_user = Depends(get_current_user),
        service: AuthService = Depends(get_auth_service)
):
    return await service.logout(refresh_token, current_user)


@router.post("/refresh")
async def refresh_user(
        refresh_token: str,
        current_user = Depends(get_current_user),
        service: AuthService = Depends(get_auth_service)
):
    return await service.refresh(refresh_token, current_user)