# Disability Max Ratings API

[![Tests](https://github.com/department-of-veterans-affairs/disability-max-ratings-api/actions/workflows/test-code.yml/badge.svg)](https://github.com/department-of-veterans-affairs/disability-max-ratings-api/actions/workflows/test-code.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/3cdea963cb3092674df1/maintainability)](https://codeclimate.com/github/department-of-veterans-affairs/disability-max-ratings-api/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3cdea963cb3092674df1/test_coverage)](https://codeclimate.com/github/department-of-veterans-affairs/disability-max-ratings-api/test_coverage)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
![Python Version from PEP 621 TOML](https://img.shields.io/badge/Python-3.12-blue)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Linting: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository uses CodeClimate for code coverage and maintainability reporting. See [Configuration Guide](docs/CONFIGURATION.md) for setup instructions.

> **Note:** This API was formerly known as Max CFI (Claim for Increase) API. All functionality remains the same.

`/disability-max-ratings` maps a list of disabilities to their max ratings, if any.

## Getting started

### Install Python3.12.3

If you're on a Mac, you can use pyenv to handle multiple python versions

```bash
brew install pyenv
pyenv install 3.12.3
pyenv global 3.12.3 # or don't do this if you want a different version available globally for your system
```

### Install Poetry

This project uses [Poetry](https://python-poetry.org/docs/) to manage dependencies.

Follow the directions on the [Poetry website](https://python-poetry.org/docs/#installation) for installation.

### Create a virtual env (Optional)

By default, Poetry will create its own virtual environment (see [here](https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment)), but it will
also detect and respect an existing virtual environment if you have one activated.

#### Other options

* Create a virtual environment with python and activate it like so:

  ```bash
  python -m venv ~/.virtualenvs/domain-ee # or wherever you want
  source ~/.virtualenvs/domain-ee/bin/activate
  ```

* Use [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to create and activate virtual environments with `pyenv`.
* Use [Poetry](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment) to explicitly create and use a virtual environment.

Make sure your python path is set up to pull from your virtualenv:

```bash
which python
# /path/to/your/virtualenv/bin/python
```

### Install dependencies

Use Poetry to run and install all dependencies:

```bash
poetry install
```

### Install pre-commit hooks

This project uses pre-commit hooks to ensure code quality. To install them, run:

```bash
poetry run pre-commit install
```

To run the pre-commit hooks at any time, run the following command:

```bash
poetry run pre-commit run --all-files
```

## Run the server locally

Using Poetry, run the following command from the root of the repository:

```bash
poetry run uvicorn src.python_src.api:app --port 8130 --reload
```

## Run with Docker

You can also run the service using Docker:

1. Build & Start Services

   ```bash
   docker compose down
   docker compose build --no-cache
   docker compose up -d
   docker compose ps
   ```

   Expected: `disability-max-ratings-api` running on port 8130

2. Check Endpoints

   ```bash
   # API docs
   curl http://localhost:8130/docs

   # Health endpoint
   curl http://localhost:8130/health

   # Main endpoint
   curl -X POST 'http://localhost:8130/disability-max-ratings' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{"diagnostic_codes": [6260]}'
   ```

   Expected main endpoint response:

   ```json
   {
       "ratings": [
           { "diagnostic_code": 6260, "max_rating": 10 }
       ]
   }
   ```

3. View API documentation:

  ```bash
  curl http://localhost:8130/docs
  ```

4. Development Environment

   ```bash
   # Run tests inside container using Poetry
   docker compose run --rm api poetry run pytest

   # Check user
   docker compose run --rm api id
   ```

   Expected: All tests pass (>80% coverage), user should be non-root (uid=1000)

### Notes on usage

#### Requests

* The `diagnostic_codes` array in the request are integers within the range of `5000 - 10000`.
  * Any request with an any entry that falls outside the range `5000 - 10000` will yield a `400`.
* An invalid request such as missing/invalid field will result in `422` status code.
* Duplicate entries in the `diagnostic_codes` array will yield a ratings array with unique entries.
* An empty `diagnostic_codes` array will yield an empty ratings array.
* A `diagnostic_codes` array with more than 1000 entries will yield a `422` status code.

#### Response

* The response contains a `ratings` array where each item contains a `diagnostic_code` and the associated `max_rating`.
  * The `diagnostic_code` corresponds to an entry in the requests `diagnostic_codes` array.
  * The `max_rating` item is a percentage expressed as an integer in the range of `0 - 100`.
* Each entry in `diagnostic_codes` array of the request with an associated max rating will yield an item in
  the `ratings` array of the response body.
* If any entry of the `diagnostic_codes` is not found, the response `ratings` array will not contain the corresponding
  item.

## Run Unit tests

Using Poetry, run the following command from the root of the repository:

```bash
poetry run pytest
```

## Contributing

Follow steps for getting started above, then make your changes and submit a pull request.

## Building docs

Swagger docs can be viewed by running the server [locally](#run-the-server-locally) and navigating to `http://localhost:8130/docs`.

If desired, the docs can be exported to `openapi.json` by running the following command:

```bash
poetry run python src/python_src/pull_api_documentation.py
```

## Repository History

NOTE: this repository was split from [abd-vro](https://github.com/department-of-veterans-affairs/abd-vro/tree/develop/domain-ee/ee-max-cfi-app).

## Automated Dependency Updates

This repository uses Dependabot to keep dependencies up to date. Pull requests from Dependabot are automatically merged if:
- All checks pass
- The update is a minor or patch version change (major version updates require manual review)
