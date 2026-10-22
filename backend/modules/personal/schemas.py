from pydantic import EmailStr, BaseModel

from database.enum import StatusType


class ProfileResponse(BaseModel):
    email: EmailStr
    status: StatusType