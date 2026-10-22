from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from modules.companies.service import CompanyService


@pytest.mark.asyncio
async def test_delete_company_runtime_error():
    # Arrange: подготовка сервиса и имитация сбоя репозитория
    session = AsyncMock()
    cache = AsyncMock()

    service = CompanyService(session=session, cache=cache)
    service.repo = AsyncMock()

    service.repo.delete_company.side_effect = RuntimeError("Database Error")

    member = SimpleNamespace(company_id=42)

    # Act: вызываем метод и перехватываем ожидаемую ошибку
    with pytest.raises(HTTPException) as exc_info:
        await service.delete_company(member)

    # Assert: проверяем ошибку и обработку транзакции
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Failed to delete company"

    service.repo.delete_company.assert_awaited_once_with(42)
    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()
    cache.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_company_access():
    session = AsyncMock()
    cache = AsyncMock()

    service = CompanyService(session=session, cache=cache)
    service.repo = AsyncMock()

    member = SimpleNamespace(company_id=1)
    params = SimpleNamespace(name="New Name")

    result = await service.update_company(member, params)

    service.repo.update_company.assert_awaited_once_with(1, params)

    session.commit.assert_awaited_once()
    session.rollback.assert_not_awaited()

    cache.delete.assert_awaited_once_with("company:1")

    assert result == {
        "company_id": 1,
        "message": "Company updated successfully"
    }


@pytest.mark.asyncio
async def test_update_company_runtime_error():
    session = AsyncMock()
    cache = AsyncMock()

    service = CompanyService(session=session, cache=cache)
    service.repo = AsyncMock()

    service.repo.update_company.side_effect = RuntimeError("Database Error")

    member = SimpleNamespace(company_id=1)
    params = SimpleNamespace(name="New Name")

    with pytest.raises(RuntimeError, match="Database Error"):
        await service.update_company(member, params)


    service.repo.update_company.assert_awaited_once_with(1, params)

    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()
    cache.delete.assert_not_awaited()


@pytest.mark.asyncio
async def test_http_update_company_integrity_error():
    session = AsyncMock()
    cache = AsyncMock()

    service = CompanyService(session=session, cache=cache)
    service.repo = AsyncMock()

    service.repo.update_company.side_effect = IntegrityError(
        statement="UPDATE companies SET name = ...",
        params={},
        orig=Exception("Constraint violation"),
    )

    member = SimpleNamespace(company_id=1)
    params = SimpleNamespace(name="New Name")

    with pytest.raises(HTTPException) as exc_info:
        await service.update_company(member, params)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Failed to update company"

    service.repo.update_company.assert_awaited_once_with(1, params)

    session.rollback.assert_awaited_once()
    session.commit.assert_not_awaited()
    cache.delete.assert_not_awaited()