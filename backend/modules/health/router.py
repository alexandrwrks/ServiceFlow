import asyncio

from fastapi import APIRouter, Response, status

from modules.health.deps import check_database_conn, check_redis_conn

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "alive"}


@router.get("/ready", status_code=status.HTTP_200_OK)
async def ready(response: Response):
    """
    :return: 200 OK, если все зависимости доступны.
             503 Service Unavailable, если хотя бы одна зависимость лежит.
    """
    db_ok, redis_ok = await asyncio.gather(
        check_database_conn(),
        check_redis_conn()
    )

    report_status = {
        "status": "ready",
        "components": {
            "database": "up" if db_ok else "down",
            "redis": "up" if redis_ok else "down",
        }
    }

    if not db_ok or not redis_ok:
        report_status["status"] = "not ready"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return report_status