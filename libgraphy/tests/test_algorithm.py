import unittest
import pytest

from libgraphy import *

class TestAlgorithm(unittest.TestCase):
    def test_dijkstra(self):
        # Example comes from "Introduction to Algorithms" (Fourth Edition) Figure 22.6 - page: 621
        vertices = [Vertex(l) for l in "stxyz"]
        s, t, x, y, z = vertices

        res_edges = [Edge(s, y, 5), Edge(y, t, 3), Edge(t, x)]

        edges = [Edge(s, t, 10), Edge(t, y, 2), Edge(y, x, 9),
                 Edge(x, z, 4), Edge(z, x, 6), Edge(z, s, 7),
                 Edge(y, z, 2)] + res_edges

        g = Graph()
        for v in vertices:
            g += v

        for e in edges:
            g += e

        route: Route = g.findPath(AlgorithmEnum.DJIKSTRA, s, x)
        assert route.edges == res_edges
        assert route.value == sum(e.value for e in res_edges)
