from fastapi import APIRouter, Depends, status

from database.enum import MembersRole
from database.models import Users, CompanyMembers
from modules.auth.deps import (
    RefreshTokenContext,
    get_auth_service,
    get_current_user,
    get_current_user_refresh_token,
)
from modules.auth.schemas import LoginUserSchema, InvitationSchema, NewPasswordSchema, RegisterUserSchema
from modules.auth.service import AuthService
from modules.employees.deps import check_roles_without_company_id

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register new user"
)
async def register_user(
        params: RegisterUserSchema,
        service: AuthService = Depends(get_auth_service)
):
    return await service.register_new_user(params)


@router.post(
    "/employees/invitations",
    status_code=status.HTTP_201_CREATED,
    summary="Invite new employee"
)
async def register_employee(
        params: InvitationSchema,
        owner_user: CompanyMembers = Depends(
            check_roles_without_company_id(
                MembersRole.OWNER,
                MembersRole.MANAGER,
            )
        ),
        service: AuthService = Depends(get_auth_service),
):
    return await service.register_new_employee(params, owner_user)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Login user"
)
async def login_user(
        params: LoginUserSchema,
        service: AuthService = Depends(get_auth_service)
):
    return await service.login(params)


@router.post(
    "/logout",
    summary="Logout user"
)
async def logout_user(
        current_user: Users = Depends(get_current_user),
        service: AuthService = Depends(get_auth_service)
):
    return await service.logout(current_user.id)


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Refresh user's token"
)
async def refresh_user(
        refresh_context: RefreshTokenContext = Depends(
            get_current_user_refresh_token
        ),
        service: AuthService = Depends(get_auth_service)
):
    return await service.refresh(
        refresh_context.token,
        refresh_context.user,
    )


@router.post(
    "/employees/invitations/{token}/activate",
    status_code=status.HTTP_200_OK,
    summary="Activate an employee invitation"
)
async def activate_employee(
        token: str,
        params: NewPasswordSchema,
        service: AuthService = Depends(get_auth_service)
):
    return await service.accept_employee_invitation(token, params.new_password)


