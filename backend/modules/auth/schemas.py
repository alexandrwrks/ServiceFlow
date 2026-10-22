from pydantic import BaseModel, EmailStr, ConfigDict, model_validator, ValidationError, Field, field_validator

from database.enum import EMPLOYEES_ROLES
from database.models import MembersRole


class RegisterCompanySchema(BaseModel):
    name: str
    description: str | None = None
    phone: str | None = None
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class RegisterUserSchema(BaseModel):
    email: EmailStr
    password: str
    retry_password: str

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        return password

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.retry_password:
            raise ValueError("Password does not match")

        return self

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterCompanyRequest(BaseModel):
    company: RegisterCompanySchema
    owner: RegisterUserSchema


class InvitationSchema(BaseModel):
    email: EmailStr  
    password: str

    first_name: str #
    last_name: str #
    phone: str | None = Field(default=None) #

    role: MembersRole

    @model_validator(mode="after")
    def check_member_role(self):
        if self.role not in EMPLOYEES_ROLES:
            raise ValueError("Role not valid")

        return self

class NewPasswordSchema(BaseModel):
    new_password: str
    new_password_confirm: str

    @model_validator(mode="after")
    def check_similar_password(self):
        if self.new_password != self.new_password_confirm:
            raise ValueError("Passwords do not match")

        return self