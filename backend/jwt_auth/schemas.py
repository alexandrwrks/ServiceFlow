from enum import StrEnum

from pydantic import BaseModel

from database.models import MembersRole


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class TokenData(BaseModel):
    user_id: int
    # role: MembersRole
    # company_id: int


class ResponseTokensSchema(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"