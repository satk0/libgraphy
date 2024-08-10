import unittest
import pytest

from libgraphy import Vertex, Edge, Graph

class TestEdge(unittest.TestCase):
    def test_edge_mult(self):
        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 10)
        e1 *= 10

        assert e1.value == 100

        e2 = e1 * 10

        assert e2.value == 1000 
        assert e1 != e2

    def test__graph__iadd__(self):
        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 10)

        g = Graph()

        g += v1
        g += v2

        g += e1

        assert g.edges == [e1]
        assert e1.graph == g
        assert e1.predecessor.neighbors == [e1.successor]
        assert e1.successor.neighbors == [e1.predecessor]

        e2 = Edge(v1, v2, 10)
        f = g + e2

        assert len(f.edges) == 2
        assert f.edges[1] == e2
        assert f.edges[0].graph == f
        assert e2.graph == f
