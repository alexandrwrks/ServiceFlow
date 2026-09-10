import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        base_url="http://test", transport=ASGITransport(app)
    ) as client:
        yield client
