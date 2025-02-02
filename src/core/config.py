import os
from pathlib import Path

from typing import List, Union, Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import (
    Field,
    model_validator
)

BASE_DIR = Path(os.path.dirname(os.path.dirname(__file__)))

class Base(BaseSettings):

    model_config = SettingsConfigDict(
        env_file = os.path.join(BASE_DIR.parent, '.env'),
        env_file_encoding = 'utf-8'
    )

class MongoSettings(Base):
    db_name: str

    protocol: str = "mongodb"
    username: str = Field(validation_alias = "MONGO_INITDB_ROOT_USERNAME")
    password: str = Field(validation_alias = "MONGO_INITDB_ROOT_PASSWORD")
    host: str = '127.0.0.1'
    port: int = 27017
    path: str = 'admin'

    dsn: str = ''

    @model_validator(mode='after')
    def create_dsn(self) -> 'MongoSettings':
        self.dsn = "{protocol}://{username}:{password}@{host}:{port}/{path}".format(
            username = self.username,
            password = self.password,
            protocol = self.protocol,
            host = self.host,
            port = self.port,
            path = self.path,
        )
        return self

    model_config = SettingsConfigDict(
        env_prefix = 'MONGO_', extra = 'ignore'
    )


class Settings(BaseSettings):
    API_URL: str = "https://api.cian.ru/search-engine/v1/search-offers-mobile-site/"
    MAX_PAGES: int = 48
    BASE_DIR: Path = BASE_DIR

    mongo: MongoSettings = MongoSettings()


settings = Settings()
