from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status

from app.jwt.schemas import TokenData, TokenType, ResponseTokensSchema
from app.utils.logger import logger
from app.utils.settings import settings


class JWTService:
    def __init__(self):
        self.ALGORITHM = settings.ALGORITHM
        self.ACCESS_TOKEN_MINUTES = settings.ACCESS_TOKEN_MINUTES
        self.REFRESH_TOKEN_DAYS = settings.REFRESH_TOKEN_DAYS
        self.SECRET_API_KEY = settings.SECRET_API_KEY

    def create_token(self, data: TokenData, token_type: TokenType, now: datetime, time_delta: timedelta) -> str:
        payload = {
            "sub": str(data.user_id),
            "role": data.role,
            "company_id": str(data.company_id),
            "token_type": token_type.value,
            "exp": now + time_delta,
            "iat": now,
        }

        return jwt.encode(
            payload,
            self.SECRET_API_KEY,
            algorithm=self.ALGORITHM,
        )

    def get_tokens(self, data: TokenData):
        now = datetime.now(timezone.utc)
        return ResponseTokensSchema(
            access_token=self.create_access_token(data, now),
            refresh_token = self.create_refresh_token(data, now),
        )

    def create_access_token(self, data: TokenData, now: datetime) -> str:
        return self.create_token(
            data=data,
            token_type=TokenType.ACCESS,
            now=now,
            time_delta=timedelta(minutes=self.ACCESS_TOKEN_MINUTES)
        )

    def create_refresh_token(self, data: TokenData, now: datetime) -> str:
        return self.create_token(
            data=data,
            token_type=TokenType.REFRESH,
            now=now,
            time_delta=timedelta(days=self.REFRESH_TOKEN_DAYS)
        )

    def verify_token(self, credentials: str):
        try:
            return jwt.decode(
                credentials, settings.SECRET_API_KEY, algorithms=[self.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            logger.warning("Access token expired")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )

        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    def verify_token_type(self, payload: dict[str, Any], token_type: TokenType) -> dict[str, Any]:
        user_id = payload.get("sub")

        if user_id is None:
            logger.warning("Invalid payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid payload",
            )

        if payload.get("token_type") != token_type:
            logger.warning("Invalid token type")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        return payload

    def access_token_expired(self, credentials: str) -> dict[str, Any]:
        payload = self.verify_token(credentials)
        return self.verify_token_type(payload, TokenType.ACCESS)

    def verify_refresh_token(self, credentials: str) -> dict[str, Any]:
        payload = self.verify_token(credentials)
        return self.verify_token_type(payload, TokenType.REFRESH)


jwt_service = JWTService()