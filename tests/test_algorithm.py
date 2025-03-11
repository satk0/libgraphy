import unittest
import pytest

from libgraphy import *
from .utils import create_test_graph

class TestAlgorithm(unittest.TestCase):
    def test_dijkstra(self):
        g = create_test_graph()
        s, x = g.vertices[0], g.vertices[2]
        res_edges = [g.edges[0], g.edges[1], g.edges[2]]

        route: Route = g.findPath(AlgorithmEnum.DIJKSTRA, s, x)
        assert route.edges == res_edges
        assert route.value == sum(e.value for e in res_edges)
