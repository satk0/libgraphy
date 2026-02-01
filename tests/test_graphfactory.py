import getopt
import random

from libgraphy import GraphFactory, AlgorithmEnum
from libgraphy.heuristic import INFINITY


def test_graph():
    # Create deterministic graph
    random.seed(8008135)
    g = GraphFactory.graph(100, weighted=True)

    # Assert basic parameters
    assert len(g.vertices) == 100
    assert len(g.edges) == 3802

    # Assert mutual vertice connection
    for v1 in g.vertices:
        for v2 in v1.neighbors:
            assert v2.isConnected(v1)

    # Assert weighted edge values
    last_value = 0
    last_last_value = -1
    for e in g.edges:
        assert e.value != last_value or last_value != last_last_value
        last_last_value = last_value
        last_value = e.value

    # Assert same edge values in both directions
    for v1 in range(len(g.vertices)-1):
        for v2 in range(v1,len(g.vertices)):
            if g.edges[(v1,v2)] != None:
                assert g.edges[(v1,v2)].value == g.edges[(v2,v1)].value


def test_complete_graph():
    # Create deterministic graph
    random.seed(8008135)
    g1 = GraphFactory.complete_graph(100, weighted=True)
    random.seed(8008135)
    g2 = GraphFactory.graph(100, edge_number=9900, weighted=True)

    # Assert basic parameters
    assert len(g1.vertices) == 100
    assert len(g1.edges) == 9900

    # Compare graph size
    assert len(g1.vertices) == len(g2.vertices)
    assert len(g1.edges) == len(g2.edges)

    # Compare graph edges
    for e in range(len(g1.edges)):
        assert (g1.edges[e].predecessor.name == g2.edges[e].predecessor.name
                and g2.edges[e].successor.name == g2.edges[e].successor.name)

def test_digraph():
    # Create deterministic graph
    random.seed(8008135)
    g = GraphFactory.digraph(100, weighted=True)

    # Assert basic parameters
    assert len(g.vertices) == 100
    assert len(g.edges) == 3802

    # Assert weighted edge values
    last_value = 0
    last_last_value = -1
    for e in g.edges:
        assert e.value != last_value or last_value != last_last_value
        last_last_value = last_value
        last_value = e.value

    # Assert different edge values in both directions
    for v1 in g.vertices:
        for v2 in v1.neighbors:
            assert g.edges[(v2,v1)] == None or g.edges[(v1,v2)].value != g.edges[(v2,v1)].value


def test_complete_digraph():
    # Create deterministic graph
    random.seed(8008135)
    g1 = GraphFactory.complete_digraph(100, weighted=True)
    random.seed(8008135)
    g2 = GraphFactory.digraph(100, edge_number=9900, weighted=True)

    # Assert basic parameters
    assert len(g1.vertices) == 100
    assert len(g1.edges) == 9900

    # Compare graph size
    assert len(g1.vertices) == len(g2.vertices)
    assert len(g1.edges) == len(g2.edges)

    # Compare graph edges
    for v1 in g1.vertices:
        for v2 in v1.neighbors:
            assert g1.edges[(v1,v2)].value != g1.edges[(v2,v1)].value


def test_grid():
    # Create deterministic grid
    random.seed(8008135)
    g = GraphFactory.grid(100, 5)

    # Assert basic parameters
    assert len(g.vertices) == 100
    assert len(g.edges) == 500

    # Assert vertice degrees
    for v in g.vertices:
        assert len(v.neighbors) == 5

    # Assert edge values are valid
    for e in g.edges:
        assert e.value == 1

    # Assert whether traits are correct
    assert g.traits().is_grid == True
    assert g.traits().grid_level == 5


def test_square_grid():
    # Create deterministic grid
    random.seed(8008135)
    g = GraphFactory.square_grid(9, 10, -1, False)

    # Assert basic parameters
    assert len(g.vertices) == 90
    assert len(g.edges) == 120

    # Assert edge values are valid
    for e in g.edges:
        assert e.value == 1

    # Assert whether traits are correct
    assert g.traits().is_grid == True
    assert g.traits().grid_level == 4


def test_triangle_grid():
    # Create deterministic grid
    random.seed(8008135)
    g = GraphFactory.triangle_grid(9, 10, -1)

    # Assert basic parameters
    assert len(g.vertices) == 90
    assert len(g.edges) == 434

    # Assert edge values are valid
    for e in g.edges:
        assert e.value == 1

    # Assert whether traits are correct
    assert g.traits().is_grid == True
    assert g.traits().grid_level == 6

from libgraphy.heuristic import *
def test_maze():
    # Create deterministic grid
    random.seed(8008135)
    g = GraphFactory.maze(100)

    # Assert basic parameters
    assert len(g.vertices) == 100
    assert len(g.edges) == 198

    # Assert edge values are valid
    for e in g.edges:
        assert e.value == 1

    # Assert whether path exists
    assert g.traits().grid_level == 4
    assert g.find_path(g.vertices[29], g.vertices[51], algorithm=AlgorithmEnum.DIJKSTRA).value == 8

def test_square_grid_maze():
    # Create deterministic grid
    random.seed(8008135)
    g = GraphFactory.square_grid_maze(9, 10)

    # Assert basic parameters
    assert len(g.vertices) == 90
    assert len(g.edges) == 178

    # Assert every vertice is connected
    for v in g.vertices:
        assert len(v.neighbors) > 0

    # Assert edge values are valid
    for e in g.edges:
        assert e.value == 1

    # Assert whether path exists
    assert g.traits().grid_level == 4

    # Assert whether maze is traversable
    for v_start in range(len(g.vertices)-1):
        for v_end in range(v_start+1, len(g.vertices)):
            assert g.find_path(g.vertices[v_start], g.vertices[v_end]).value != INFINITY


def test_ring():
    # Create deterministic grid
    random.seed(8008135)
    g = GraphFactory.ring(100, True)

    # Assert basic parameters
    assert len(g.vertices) == 100
    assert len(g.edges) == 100

    # Assert every vertice is connected
    for v in g.vertices:
        assert len(v.neighbors) == 1

    # Assert edge values are valid
    for e in g.edges:
        assert e.value == 1

    # Check whether the ring loops
    visited = []
    v = g.vertices[0].neighbors[0]
    while v != g.vertices[0]:
        if v in visited:
            assert False
        visited.append(v)
        v = v.neighbors[0]
    assert True
