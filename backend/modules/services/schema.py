from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class CreateNewService(BaseModel):
    name: str = Field(min_length=10, max_length=150)
    description: str = Field(max_length=1500)
    base_price: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)
    duration_minutes: int | None = Field(default=None)

    @model_validator(mode="after")
    def fields_validator(self):
        self.name = " ".join(self.name.split())

        if self.duration_minutes is not None:
            if self.duration_minutes < 0:
                raise ValueError("duration_minutes cannot be negative")

        return self


class UpdateService(BaseModel):
    name: str | None = Field(default=None, max_length=150)
    description: str | None = Field(default=None, max_length=1500)
    base_price: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    duration_minutes: int | None = Field(default=None)

    @model_validator(mode="after")
    def fields_validator(self):
        if self.name is not None:
            self.name = " ".join(self.name.split())

        if self.description is not None:
            self.description = " ".join(self.description.split())

        if self.base_price is not None:
            if self.base_price < 0:
                raise ValueError("base_price cannot be negative")

            if self.base_price.as_tuple().exponent < -2:
                raise ValueError("base_price cannot have more than 2 decimal places")

        if self.duration_minutes is not None:
            if self.duration_minutes < 0:
                raise ValueError("duration_minutes cannot be negative")

        return self
