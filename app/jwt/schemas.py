from enum import StrEnum

from pydantic import BaseModel


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class TokenData(BaseModel):
    user_id: str
    role: str
    company_id: str


class ResponseTokensSchema(BaseModel):
    access_token: str
    refresh_token: str
    type: str = "Bearer"