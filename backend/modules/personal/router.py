from fastapi import APIRouter, Depends, status

from database.models import Users
from modules.auth.deps import get_current_user
from modules.personal.deps import get_personal_service
from modules.personal.schemas import ProfileResponse
from modules.personal.service import PersonalService

router = APIRouter()


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user's profile",
    response_model=ProfileResponse
)
async def get_me(
        current_user: Users = Depends(get_current_user),
        service: PersonalService = Depends(get_personal_service)
):
    return service.get_personal_stat(current_user)