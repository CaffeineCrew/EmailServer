from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


config = get_settings()