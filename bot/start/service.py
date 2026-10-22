import httpx

async def telegram_api_activate(
    token: str,
    telegram_id: int
) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="http://api:8000/telegram/activate",
            params={
                "token": token,
                "telegram_id": telegram_id
            }
        )
        response.raise_for_status()

        if response.status_code == 201:
            return True

        return False