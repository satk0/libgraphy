import unittest
import pytest

from libgraphy import *
from .utils import create_hexagonal_flat_graph, create_test_graph, create_grid_graph, create_octogonal_graph

class TestAlgorithm(unittest.TestCase):
    def test_dijkstra(self):
        g = create_test_graph()
        s, x = g.vertices[0], g.vertices[2]
        res_edges = [g.edges[0], g.edges[1], g.edges[2]]

        path: Path = g.find_path(s, x, algorithm = AlgorithmEnum.DIJKSTRA)
        assert path.edges == res_edges
        assert path.value == sum(e.value for e in res_edges)

    def test_bellman_ford(self):
        vertices = [Vertex(l) for l in "stxyz"]
        s, t, x, y, z = vertices

        edges = [Edge(s, t, 6), Edge(s, y, 7),
                 Edge(t, x, 5), Edge(t, y, 8),
                 Edge(t, z, -4), Edge(y, x, -3),
                 Edge(y, z, 9), Edge(x, t, -2),
                 Edge(z, x, 7), Edge(z, s, 2)]

        g = Graph()
        for v in vertices:
            g += v

        for e in edges:
            g += e

        res_edges = [g.edges[1], g.edges[5], g.edges[7], g.edges[4]]

        path: Path = g.find_path(s, z, algorithm = AlgorithmEnum.BELLMAN_FORD)
        assert path.edges == res_edges
        assert path.value == sum(e.value for e in res_edges)

    def test_a_star_grid(self):
        g: Graph = create_grid_graph(10, 13)

        s, t = [g.vertices[0], g.vertices[-5]]

        path: Path = g.find_path(s, t, ManhattanDistance(), AlgorithmEnum.A_STAR)

        # To fix: print(repr(str(path)))
        assert repr(path) == "Path: 0,0 -> 1,0 -> 2,0 -> 3,0 -> 4,0 -> 5,0 -> 6,0 -> 7,0 -> 8,0 -> 8,1 -> 8,2 -> 8,3 -> 8,4 -> 8,5 -> 8,6 -> 8,7 -> 8,8 -> 8,9\nValue: 17"
        assert path.value == 17

        path: Path = g.find_path(s, t, algorithm = AlgorithmEnum.DIJKSTRA)
        assert path.value == 17

    def test_a_star_hexagonal(self):
        g: Graph = create_hexagonal_flat_graph(8, 5)

        s, t = [g.vertices[0], g.vertices[-3]]

        path: Path = g.find_path(s, t, HexagonalManhattanDistance(), AlgorithmEnum.A_STAR)

        # To fix: print(repr(str(path)))
        assert repr(path) == "Path: 0,0 -> 0,1 -> 0,2 -> 0,3 -> 0,4 -> 0,5 -> 1,5 -> 1,6 -> 2,7\nValue: 8"
        assert path.value == 8

        path: Path = g.find_path(s, t, algorithm = AlgorithmEnum.DIJKSTRA)
        assert path.value == 8

    def test_a_star_octogonal(self):
        g: Graph = create_octogonal_graph(16, 24)

        s, t = [g.vertices[0], g.vertices[-3]]

        path: Path = g.find_path(s, t, ChebyshevDistance(), AlgorithmEnum.A_STAR)

        # To fix: print(repr(str(path)))
        assert repr(path) == "Path: 0,0 -> 1,0 -> 2,0 -> 3,0 -> 4,0 -> 5,0 -> 6,0 -> 7,1 -> 8,2 -> 9,3 -> 10,4 -> 11,5 -> 12,6 -> 13,7 -> 14,8 -> 15,9 -> 16,10 -> 17,11 -> 18,12 -> 19,13 -> 20,14 -> 21,15\nValue: 21"
        assert path.value == 21

        path: Path = g.find_path(s, t, algorithm = AlgorithmEnum.DIJKSTRA)
        assert path.value == 21

    def test_best_negative(self):
        # TODO: Move this to utils
        vertices = [Vertex(l) for l in "stxyz"]
        s, t, x, y, z = vertices

        edges = [Edge(s, t, 6), Edge(s, y, 7),
                 Edge(t, x, 5), Edge(t, y, 8),
                 Edge(t, z, -4), Edge(y, x, -3),
                 Edge(y, z, 9), Edge(x, t, -2),
                 Edge(z, x, 7), Edge(z, s, 2)]

        g = Graph()
        for v in vertices:
            g += v

        for e in edges:
            g += e

        res_edges = [g.edges[1], g.edges[5], g.edges[7], g.edges[4]]

        path: Path = g.find_path(s, z)
        assert path.edges == res_edges
        assert path.value == sum(e.value for e in res_edges)

    def test_best_a_star(self):
        g: Graph = create_octogonal_graph(16, 24)

        s, t = [g.vertices[0], g.vertices[-3]]

        path: Path = g.find_path(s, t, heuristic=ChebyshevDistance())

        # To fix: print(repr(str(path)))
        assert repr(path) == "Path: 0,0 -> 1,0 -> 2,0 -> 3,0 -> 4,0 -> 5,0 -> 6,0 -> 7,1 -> 8,2 -> 9,3 -> 10,4 -> 11,5 -> 12,6 -> 13,7 -> 14,8 -> 15,9 -> 16,10 -> 17,11 -> 18,12 -> 19,13 -> 20,14 -> 21,15\nValue: 21"
        assert path.value == 21

    def test_best_dijkstra(self):
        g = create_test_graph()
        s, x = g.vertices[0], g.vertices[2]
        res_edges = [g.edges[0], g.edges[1], g.edges[2]]

        path: Path = g.find_path(s, x)
        assert path.edges == res_edges
        assert path.value == sum(e.value for e in res_edges)
