from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, model_validator

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

    @model_validator(mode="after")
    def check_similar_password(self):
        if self.new_password != self.new_password_confirm:
            raise ValueError("Passwords do not match")

        return self.new_password