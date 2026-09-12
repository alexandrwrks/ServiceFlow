from enum import StrEnum

from pydantic import BaseModel


class TokenType(StrEnum):
    ACCESS = "ACCESS"
    REFRESH = "REFRESH"


class TokenData(BaseModel):
    user_id: int
    role: str
    company_id: int