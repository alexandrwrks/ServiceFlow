from pydantic import BaseModel, Field

from app.database.models import UserRole


class NewUserParams(BaseModel):
    new_role: UserRole | None = Field(default=None)