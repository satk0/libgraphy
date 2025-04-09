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
