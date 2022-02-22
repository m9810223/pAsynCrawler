rm -rf dist

POETRY_HTTP_BASIC_PYPI_USERNAME=__token__ poetry publish -vvv --build
