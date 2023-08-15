from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    validator,
)

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class Environment(StrEnum):
    dev = "dev"
    prod = "prod"


class Paths:
    # demo_template
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / "app"
    EMAIL_TEMPLATES_DIR: Path = BASE_DIR / "emails"
    LOGIN_PATH: str = "/auth/login"


class Settings(BaseSettings):
    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = "dev"
    SECRET_KEY: str
    DEBUG: bool = False
    AUTH_TOKEN_LIFETIME_SECONDS = 3600
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"  # type:ignore
    PAGINATION_PER_PAGE: int = 20

    REDIS_URL: RedisDsn

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_URI: PostgresDsn

    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    DEFAULT_FROM_EMAIL: EmailStr
    DEFAULT_FROM_NAME: str | None = None
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, _: bool, values: dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("DEFAULT_FROM_EMAIL")
        )

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
