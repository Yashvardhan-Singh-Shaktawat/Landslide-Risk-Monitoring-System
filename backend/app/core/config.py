from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "LandslideNER Backend API"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    DISCLAIMER: str = (
        "Educational/academic prototype. Not an official warning system. "
        "For official alerts follow NDMA, IMD, GSI and the State Disaster Management Authorities."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
