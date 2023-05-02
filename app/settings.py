from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, SecretStr, validator


class Settings(BaseSettings):
    """Настройки."""

    WEATHER_KEY: str
    GEOCODER_KEY: str

    POSTGRES_USER: str = 'postgres'
    POSTGRES_PASSWORD: SecretStr = SecretStr('postgres')
    POSTGRES_HOST: str = 'localhost'
    POSTGRES_PORT: str = '5432'
    POSTGRES_DB: str = 'postgres'

    POSTGRES_URI: Optional[PostgresDsn]

    @validator('POSTGRES_URI', pre=True)
    def build_uri(cls, uri: Optional[PostgresDsn], values: Dict[str, Any]) -> Any:
        """Создание адреса Postgres."""
        return uri or PostgresDsn.build(
            scheme='postgresql',
            user=values['POSTGRES_USER'],
            password=values['POSTGRES_PASSWORD'].get_secret_value(),
            host=values['POSTGRES_HOST'],
            port=values['POSTGRES_PORT'],
            path=f"/{values['POSTGRES_DB'] or ''}",
        )

    class Config:
        env_file = '.env'
