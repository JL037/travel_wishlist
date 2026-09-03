from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict
import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SENTRY_DSN: str
    POSTGRES_DB: str
    OPEN_WEATHER_API_KEY: str
    RESEND_API_KEY: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AT Protocol OAuth (Phase 1 - see AT_PROTOCOL_MIGRATION.md). Optional so
    # existing .env files keep working until these are configured; the
    # atproto_auth router refuses to start a login until they're set.
    # ATPROTO_CLIENT_ID must be the exact public HTTPS URL this app serves
    # its client-metadata.json from (see GET /auth/atproto/client-metadata.json).
    ATPROTO_CLIENT_ID: str | None = None
    ATPROTO_CLIENT_URI: str | None = None
    ATPROTO_REDIRECT_URI: str | None = None

    model_config = ConfigDict(env_file=f".env.{ 'development' if ENVIRONMENT == 'dev' else 'production' }",
 env_file_encoding="utf-8")

settings = Settings()

