import secrets

from fastapi import APIRouter, Depends, status, HTTPException

from cache.cache_service import CacheService
from cache.redis import get_cache_service
from database.models import Users
from modules.auth.deps import get_current_user
from modules.telegram.deps import get_telegram_service
from modules.telegram.service import TelegramService
from utils.settings import settings

router = APIRouter(
    prefix="/telegram",
    tags=["Telegram"]
)


@router.post("/link")
async def create_telegram_link(
        current_user: Users = Depends(get_current_user),
        cache: CacheService = Depends(get_cache_service)
):
    token = secrets.token_urlsafe(24)

    await cache.set(
        f"telegram_link:{token}",
        str(current_user.id),
        expire=300
    )

    return {
        "url": (
            f"https://telegram.me/{settings.TELEGRAM_BOT_USERNAME}"
            f"?start={token}"
        )
    }


@router.post(
    "/activate",
    status_code=status.HTTP_201_CREATED,
)
async def activate_telegram_account(
        token: str,
        telegram_id: int,
        redis: CacheService = Depends(get_cache_service),
        service: TelegramService = Depends(get_telegram_service)
):
    user_id = await redis.get(f"telegram_link:{token}")

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Не удалось привязать телеграм аккаунт")

    print("Успешная регистрация, попозже добавлю добавление в БД")

