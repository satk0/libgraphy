## Setup
**NOTE**: Make sure you have [graphviz package](https://www.graphviz.org/download/) installed on your system!

To make sure that everything will work properly install the project via:

    poetry install --all-extras --with=dev

## Tests

Run test via:

    poetry run pytest

Check test coverage with:

    poetry run pytest --cov=libgraphy

to HTML (in `htmlcov` directory):

    poetry run pytest --cov=libgraphy --cov-report=html

## Debug libgraphy inside Jupyter:

All the notebooks are inside `/notebook` directory, you can read [notebook/README.md](notebook/README.md) to find out more about setting it up.

## Publishing

To publish a package you ought to update the version:

    poetry version patch

And then publish it (make sure you have TestPyPI set up):

    poetry publish -r testpypi --build

## Benchmark

To run benchmarks issue the following installation:

     poetry install --all-extras --with=dev,bench 
