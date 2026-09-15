from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int

    ALGORITHM: str
    ACCESS_TOKEN_MINUTES: int
    REFRESH_TOKEN_DAYS: int
    SECRET_API_KEY: str

    FRONTEND_URL: str
    SMTP_PASSWORD: str
    SMTP_USERNAME: str
    SMTP_HOST: str
    EMAIL_FROM: str = "koozma-alex@mail.ru"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        """:return: URL для рабочей БД"""
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.POSTGRES_DB}"
        )

    @property
    def ALEMBIC_DATABASE_URL(self):
        """:return: URL для работы с миграциями в рабочей БД"""
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}"
            f"/{self.POSTGRES_DB}"
        )


settings = Settings()
