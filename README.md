# Libgraphy
Directed Graph Library Project

## TODO:
* [x] - Vertex class
* [x] - Edge class
* [x] - Path class
* [x] - Graph class
* [x] - Djikstra Algorithm
* [x] - Make Edge constructor take strings as vertices names
* [x] - Graph to CSGraph/NetworkX (static method)
* [x] - CSGraph/NetworkX to Graph (static method)
* [x] - Read graph from JSON file
* [x] - Write graph to JSON file
* [x] - Check if graph is a grid
* [x] - GraphTraits class
* [ ] - A* algorithm
* [ ] - JPS algorithm

# Setup

Vizualization in libgraphy is optable.
## Default (no graph vizualization, pure algorithms):

    pip install --index-url https://test.pypi.org/simple/ libgraphy

## To work with jupyter (includes graphs vizualization):

**NOTE**: Make sure you have [graphviz package](https://www.graphviz.org/download/) installed on your system!

    pip install --index-url https://test.pypi.org/simple/ libgraphy[extras]

## Using Jupyter:

1. Create a new virtual environment (kernel).
2. Install libgraphy 
3. **Restart the kernel**.

# Contributions

Any contribution is more than welcome. If you find out that something is not working, missing or needs to be improved - feel free to make an issue about it.

Any commits to the repo would also help a lot, check [DEVELOPERS.md](DEVELOPERS.md) :)
