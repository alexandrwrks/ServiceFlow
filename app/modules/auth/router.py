from fastapi import APIRouter, Depends

from app.modules.auth.deps import get_auth_service
from app.modules.auth.schemas import RegisterUserSchema, LoginUserSchema, RegisterCompanySchema, RegisterCompanyRequest
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


@router.post("/register-employee")
async def register_employee(
        params: RegisterUserSchema,
        service: AuthService = Depends(get_auth_service)
):
    return await service.register_new_employee(params)


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