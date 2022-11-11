import functools
import typing

import pydantic


ENV_PREFIX = 'provider_a'
ENV_FILENAME = '.env'


class APISettings(pydantic.BaseSettings):
    host: str = '127.0.0.1'
    port: int = 9000
    log_level: str = 'info'
    title: str = 'Airflow service'
    swagger_url: typing.Optional[str] = '/'
    openapi_url: typing.Optional[str] = '/openapi.json'
    allowed_origins: typing.List[str] = ['127.0.0.1']

    class Config:
        env_file = ENV_FILENAME
        env_prefix = f'{ENV_PREFIX}_api_'


class RedisSettings(pydantic.BaseSettings):
    url: str = "redis://172.17.0.2"
    db: int = 0

    class Config:
        env_file = ENV_FILENAME
        env_prefix = f'{ENV_PREFIX}_redis_'


class Settings(pydantic.BaseSettings):
    debug: bool = True
    environment: str
    api: APISettings = APISettings()
    redis: RedisSettings = RedisSettings()

    class Config:
        env_file = ENV_FILENAME
        env_prefix = f'{ENV_PREFIX}_'


@functools.lru_cache()
def _get_settings() -> Settings:
    settings: Settings = Settings()

    return settings


def __getattr__(attr):
    return getattr(_get_settings(), attr)
