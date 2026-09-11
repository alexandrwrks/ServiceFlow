from pydantic import BaseModel, EmailStr, ConfigDict


class RegisterCompanySchema(BaseModel):
    name: str
    description: str | None = None
    phone: str | None = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class RegisterUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterCompanyRequest(BaseModel):
    company: RegisterCompanySchema
    owner: RegisterUserSchema