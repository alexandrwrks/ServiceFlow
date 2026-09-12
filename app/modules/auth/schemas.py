from pydantic import BaseModel, EmailStr, ConfigDict, field_validator

from app.database.models import UserRole


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


class InvitationSchema(BaseModel):
    first_name: str #
    last_name: str #

    phone: str | None = None #
    email: EmailStr  #
    password: str #
    role: UserRole #

class NewPasswordSchema(BaseModel):
    new_password: str
    new_password_confirm: str

    @field_validator("new_password", "new_password_confirm", mode="after")
    @classmethod
    def check_similar_password(cls):
        if cls.new_password != cls.new_password_confirm:
            raise ValueError("Passwords do not match")

        return cls.new_password