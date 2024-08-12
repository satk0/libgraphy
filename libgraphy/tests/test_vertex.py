import unittest
import pytest

from libgraphy import Vertex, Graph

class TestVertex(unittest.TestCase):
    def test__add__(self):
        v1 = Vertex(1)
        v2 = Vertex('2')
        v3 = Vertex()

        prev_id = id(v1)
        v1 = v1 + v2
        v4 = v1 + v3
        assert v1.neighbors == [v2]
        assert v4.neighbors == [v2, v3]
        assert v1.name == v4.name
        assert v1.value == v4.value
        assert id(v1) != prev_id

    def test__iadd__(self):
        v1 = Vertex(1)
        v2 = Vertex('2')
        v3 = Vertex()

        v1 += v2
        v3 += v1
        v3 += v2
        assert v1.neighbors == [v2]
        assert v3.neighbors == [v1, v2]

    def test_vertex__item__(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)

        v1 += v2
        v1 += v3
        assert v1.neighbors == [v2, v3]
        assert v1[1] == v3

        del v1[0]
        v1[0] = v2
        assert v1.neighbors == [v2]

    def test_vertex__str__(self):
        v = Vertex("name")
        assert v.__str__() == v.name

        v = Vertex()
        assert v.__str__() == str(id(v))

    def test_vertex_isConnected(self):
        v1 = Vertex(1)
        v2 = Vertex(2)

        v1 += v2
        assert v1.isConnected(v2) == True
        assert v2.isConnected(v1) == True
        assert v1.neighbors == [v2]
        assert v2.neighbors == []

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

