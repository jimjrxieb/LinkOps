from pydantic_settings import BaseSettings
from pydantic import Extra, Field
import os


class Settings(BaseSettings):
    # OpenAI API Key (required for LLM functionality)
    OPENAI_API_KEY: str = Field(
        default="", description="OpenAI API key for LLM functionality"
    )

    # Database Settings
    DATABASE_URL: str = Field(
        default="postgresql://linkops:linkops_password@localhost:5432/linkops",
        description="Database connection URL",
    )
    DATABASE_POOL_SIZE: int = Field(
        default=10, description="Database connection pool size"
    )
    DATABASE_MAX_OVERFLOW: int = Field(
        default=20, description="Database max overflow connections"
    )

    # Application Settings
    APP_NAME: str = Field(default="LinkOps Core", description="Application name")
    DEBUG: bool = Field(default=False, description="Debug mode")
    HOST: str = Field(default="0.0.0.0", description="Host to bind to")
    PORT: int = Field(default=8000, description="Port to bind to")
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")

    # File Storage Settings
    SCREENSHOTS_DIR: str = Field(
        default="./screenshots", description="Screenshots directory"
    )
    LOGS_DIR: str = Field(default="./logs", description="Logs directory")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = Extra.allow  # Ensures it doesn't crash on unknown env vars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate required settings
        if not self.OPENAI_API_KEY:
            print(
                "WARNING: OPENAI_API_KEY not set. " "LLM functionality will be limited."
            )

        # Create directories if they don't exist
        os.makedirs(self.SCREENSHOTS_DIR, exist_ok=True)
        os.makedirs(self.LOGS_DIR, exist_ok=True)


settings = Settings()
