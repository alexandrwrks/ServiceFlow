from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field


class NewCompanySchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=100)
    phone: str = Field(...)
    email: EmailStr = Field(...)


class UpdateCompanySchema(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)


class OwnerProfileSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None)


class CreateCompanyRequest(BaseModel):
    company: NewCompanySchema
    owner: OwnerProfileSchema


class ResponseCompany(BaseModel):
    id: int
    name: str
    description: str
    phone: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
