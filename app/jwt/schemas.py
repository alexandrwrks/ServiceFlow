from enum import StrEnum

from pydantic import BaseModel


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class TokenData(BaseModel):
    user_id: int
    role: str
    company_id: int


class ResponseTokensSchema(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"