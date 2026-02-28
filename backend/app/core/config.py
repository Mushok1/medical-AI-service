from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./medical_ai.db"
    storage_dir: Path = Path("./storage")

    model_config = SettingsConfigDict(env_file=".env", env_prefix="MEDICAL_AI_")


settings = Settings()
