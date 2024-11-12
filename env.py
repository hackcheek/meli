"""
La clase Settings permite acceder a las variables de entorno, 
reconociendolas automaticamente desde el archivo .env
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    meli_access_token: str
    openai_api_key: str

    class Config:
        env_file = '.env'


@lru_cache
def env_settings() -> Settings:
    return Settings()
