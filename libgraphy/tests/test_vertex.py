import unittest
import pytest

from libgraphy import Vertex, Graph

class TestVertex(unittest.TestCase):
    def test__add__(self):
        v1 = Vertex(1)
        v2 = Vertex()
        v3 = Vertex()

        v1 = v1 + v2
        v4 = v1 + v3

        assert len(v1.neighbors) == 1
        assert v1.neighbors[0] == v4.neighbors[0]
        assert v4.neighbors[1] == v3


    def test_vertex_add(self):
        v1 = Vertex(1)
        v2 = Vertex("2")

        v1 += v2
        v3 = v2 + v1

        assert v1.neighbors == [v2]
        assert v3.neighbors == [v1]
        assert v2 != v3

    def test_vertex_access(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)

        v1 += v2
        v1 += v3

        assert v1.neighbors == [v2, v3]
        assert v1.isConnected(v2)
        assert v1[1] == v3

        del v1[0]
        v1[0] = v2

        assert v1.neighbors == [v2]

    def test__graph__iadd__(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)

        g = Graph()

        g += v1
        g += v2
        g += v3

        assert g.vertices == [v1, v2, v3]
        assert g[0] == v1
        assert g[0].graph == g

        del g[0]
        g[0] = v1
        assert g[0] == v1

        f = g + v2
        assert len(f.vertices) == 3
        assert f.vertices[0].name == v1.name
        assert f.vertices[1].name == v3.name
        assert f.vertices[2] == v2

