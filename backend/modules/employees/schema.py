from pydantic import BaseModel, Field

from database.models import MembersRole


class NewUserParams(BaseModel):
    role: MembersRole | None = Field(default=None)
