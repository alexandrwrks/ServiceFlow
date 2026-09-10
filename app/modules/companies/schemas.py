from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class NewCompanySchema(BaseModel):
    title: str
    description: str
    phone: str
    email: EmailStr


class ResponseCompany(BaseModel):
    name: str
    description: str
    phone: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
