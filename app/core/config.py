from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, ConfigDict

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    TEST_DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

