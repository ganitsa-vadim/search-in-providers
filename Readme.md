# Airflow Provider-a Provider-b

Services for search in providers

## Requirements

* python >=3.10, <4.0

## Configuration

Projects use `.env` file or environment variables for configuration. There is an example: `.env.example`.

## Development

Steps for Development such as setup, linting and testing can be run via `make` commands.

### Setup env and install dependencies

`make setup` - creates virtual environment in `.venv/` folder and installs required packages.

#### Adding new dependencies

For dependencies management [pipenv](https://pipenv.pypa.io/) is being used.

### Lint

`make lint` - runs configured linter.

### Mypy

`make mypy` - runs configured mypy.

### Test

`make test` - runs configured pytest.  
`make testcov` - runs configured pytest and opens coverage report in browser.

### Run

create .env files

### Run in docker-compose

`docker-compose up`

#### Activate venv

`source .venv/bin/activate`

#### Run service

`make run` - runs API via uvicorn

### Clean

`make clean` - removes everything, except source code
