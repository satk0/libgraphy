import unittest
import pytest

from libgraphy import *
from .utils import create_test_graph

class TestAlgorithm(unittest.TestCase):
    def test_dijkstra(self):
        g = create_test_graph()
        s, x = g.vertices[0], g.vertices[2]
        res_edges = [g.edges[0], g.edges[1], g.edges[2]]

        path: Path = g.findPath(AlgorithmEnum.DIJKSTRA, s, x)
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

        path: Path = g.findPath(AlgorithmEnum.BELLMANFORD, s, z)
        assert path.edges == res_edges
        assert path.value == sum(e.value for e in res_edges)
