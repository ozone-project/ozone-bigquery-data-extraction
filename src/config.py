import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    google_cloud_project: str
    google_application_credentials: Optional[str] = None
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    return Settings()