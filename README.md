# LibGraphy
Directed Graph Library Project

## TODO:
* [x] - Vertex class
* [ ] - Edge class
* [ ] - Route class
* [ ] - Graph class
* [ ] - Graph to CSGraph/NetworkX (static method)
* [ ] - CSGraph/NetworkX to Graph (static method)
* [ ] - Djikstra Algorithm

# Debugging

## Using Python:

1. Create a new virtual environment in a new directory.
2. install libgraphy with:
```bash
pip install <PROJECT_DIRECTORY_PATH>
```
## Using Jupyter:

1. Create a new virtual environment (kernel).
2. Make any change to the codebase.
3. Reinstall libgraphy (as for Python) and **restart the kernel**.

# Tests

Run test via:

    python -m pytest

Check test coverage with:

    python -m pytest --cov=libgraphy

to HTML (in `htmlcov` directory):

    python -m pytest --cov=libgraphy --cov-report=html

