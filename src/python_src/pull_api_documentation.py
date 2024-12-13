import json
import os

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def export_openapi(app: FastAPI, filename: str) -> None:
    """Export the OpenAPI specification of a FastAPI app to a JSON file."""
    openapi_schema = get_openapi(title=app.title, version=app.version, routes=app.routes)

    with open(filename, 'w') as outfile:
        json.dump(openapi_schema, outfile, indent=4)


if __name__ == '__main__':
    from api import app

    if not os.path.exists('build'):
        os.mkdir('build')

    output_file = os.path.abspath('build/fastapi.json')
    export_openapi(app, output_file)
    print(f'OpenAPI specification exported to: {output_file}')
