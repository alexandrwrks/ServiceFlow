from decimal import Decimal

from pydantic import BaseModel, Field


class CreateNewService(BaseModel):
    name: str = Field(max_length=150)
    description: str = Field(max_length=1500)
    base_price: Decimal = Field(...)
    duration_minutes: int | None = Field(default=None)


class UpdateService(BaseModel):
    name: str | None = Field(default=None, max_length=150)
    description: str | None = Field(max_length=1500)
    base_price: Decimal | None = Field(default=None)
    duration_minutes: int | None = Field(default=None)