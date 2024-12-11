# Disability Max Ratings API

> **Note:** This API was formerly known as Max CFI (Claim for Increase) API. All functionality remains the same.

`/disability-max-ratings` maps a list of disabilities to their max ratings, if any.

## Getting started

### Install Python3.10

If you're on a Mac, you can use pyenv to handle multiple python versions

```bash
brew install pyenv
pyenv install python3.10
pyenv global python3.10 # or don't do this if you want a different version available globally for your system
```

### Install Poetry

This project uses [Poetry](https://python-poetry.org/docs/) to manage dependencies.

Follow the directions on the [Poetry website](https://python-poetry.org/docs/#installation) for installation.

### Create a virtual env (Optional)

By default, Poetry will create its own virtual environment (see [here](https://python-poetry.org/docs/basic-usage/#using-your-virtual-environment)), but it will
also detect and respect an existing virtual environment if you have one activated.

#### Other options:

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

## Run the server with Docker

TODO: update this to use the new disability-max-ratings-api Docker Compose file - <https://github.com/department-of-veterans-affairs/abd-vro/issues/3833>

## Testing it all together

Run the Python webserver (uvicorn command above). Now you should be able to make a post request to the `/disability-max-ratings/`
endpoint with a request body of the format:

```json
{
    "diagnostic_codes": [
        6260
    ]
}
```

This should result in a response with the following body:

```json
{
    "ratings": [
        {
            "diagnostic_code": 6260,
            "max_rating": 10
        }
    ]
}
```

### Notes on usage:

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
