import functools
import typing

import pydantic

ENV_PREFIX = 'provider_b'
ENV_FILENAME = '.env'


class APISettings(pydantic.BaseSettings):
    host: str = '127.0.0.1'
    port: int = 8000
    log_level: str = 'info'
    title: str = 'Provider-b service'
    swagger_url: typing.Optional[str] = '/'
    openapi_url: typing.Optional[str] = '/openapi.json'
    allowed_origins: typing.List[str] = ['127.0.0.1']

    class Config:
        env_file = ENV_FILENAME
        env_prefix = f'{ENV_PREFIX}_api_'


class Settings(pydantic.BaseSettings):
    debug: bool = True
    environment: str
    api: APISettings = APISettings()

    class Config:
        env_file = ENV_FILENAME
        env_prefix = f'{ENV_PREFIX}_'


@functools.lru_cache()
def _get_settings():
    settings = Settings()

    return settings


def __getattr__(attr):
    return getattr(_get_settings(), attr)
