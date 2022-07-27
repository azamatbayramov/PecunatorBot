from functools import lru_cache
from pydantic import BaseSettings


class Config(BaseSettings):
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    TELEGRAM_TOKEN: str

    def DATABASE_URL(self) -> str:
        return f"postgres://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:5432/{self.DATABASE_NAME}"


@lru_cache
def get_config():
    return Config()


config = get_config()
