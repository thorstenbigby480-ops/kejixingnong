"""配置项 —— 通过 .env 读取"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "绿脉兴农"
    APP_VERSION: str = "0.1.0"
    DATABASE_URL: str = "sqlite:///./greenpulse.db"
    SECRET_KEY: str = "change-this-in-production-please-9f8e7d"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
