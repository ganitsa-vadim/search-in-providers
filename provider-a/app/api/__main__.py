import uvicorn

from ..core import config


def main():
    uvicorn.run(
        'app.api:app',
        host=config.api.host,
        port=config.api.port,
        log_level=config.api.log_level,
        debug=config.debug,
        reload=config.debug,
    )


if __name__ == '__main__':
    main()
