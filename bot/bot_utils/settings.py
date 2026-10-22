from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    BOT_TOKEN: str
    TELEGRAM_BOT_USERNAME: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        extra="ignore"
    )


settings = Settings()