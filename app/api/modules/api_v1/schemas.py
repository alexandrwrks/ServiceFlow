from pydantic import BaseModel, EmailStr


class NewCompanySchema(BaseModel):
    title: str
    description: str
    phone: str
    email: EmailStr