"""
Application Configuration
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_prefix="MSFINTECH_", extra="ignore")
    
    PROJECT_NAME: str = "Economic Indicators Dashboard"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "economic_indicators"

    # Eulerpool Integration (Pydantic will look for MSFINTECH_EULERPOOL_API_KEY)
    EULERPOOL_API_KEY: str = "demo"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
