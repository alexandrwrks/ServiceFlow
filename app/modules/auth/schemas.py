from pydantic import BaseModel, EmailStr, ConfigDict


class RegisterCompanySchema(BaseModel):
    name: str
    email: EmailStr
    description: str | None = None
    phone: str | None = None

    model_config = ConfigDict(from_attributes=True)


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str