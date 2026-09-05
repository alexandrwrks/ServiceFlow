from fastapi import APIRouter

router = APIRouter()


@router.post("/auth/telegram")
async def telegram_auth(

):
    return await service.telegram_auth()