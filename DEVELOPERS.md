## Setup
To make sure that everything will work properly install the project via:

    poetry install --all-extras --with=dev

## Tests

Run test via:

    poetry run pytest

Check test coverage with:

    poetry run pytest --cov=libgraphy

to HTML (in `htmlcov` directory):

    poetry run pytest --cov=libgraphy --cov-report=html

