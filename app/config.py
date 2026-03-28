from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    max_file_size_mb: int = 10
    upload_dir: str = "uploads"

    class Config:
        env_file = ".env"

settings = Settings()
