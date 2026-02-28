from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./medical_ai.db"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="MEDICAL_AI_")


settings = Settings()
