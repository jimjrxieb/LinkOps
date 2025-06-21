from pydantic_settings import BaseSettings
from pydantic import Extra

class Settings(BaseSettings):
    # OpenAI API Key (required)
    OPENAI_API_KEY: str
    
    # Database Settings
    DATABASE_URL: str = "postgresql://linkops:secure_db_password_2024@localhost:5432/linkops"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Application Settings
    APP_NAME: str = "LinkOps Core"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    
    # File Storage Settings
    SCREENSHOTS_DIR: str = "./screenshots"
    LOGS_DIR: str = "./logs"

    class Config:
        env_file = ".env"
        extra = Extra.allow  # Ensures it doesn't crash on unknown env vars

settings = Settings() 