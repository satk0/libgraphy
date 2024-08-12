import unittest
import pytest

from libgraphy import Vertex, Graph

class TestVertex(unittest.TestCase):
    def test___add__(self):
        v0 = Vertex(1)
        v1 = Vertex('2')
        v2 = Vertex()

        prev_id = id(v0)
        v0 = v0 + v1
        assert v0.neighbors == [v1]
        assert v1.neighbors == []
        assert id(v0) != prev_id

        v3 = v0 + v2
        assert v3.neighbors == [v1, v2]
        assert v0.name == v3.name
        assert v0.value == v3.value

    def test___iadd__(self):
        v0 = Vertex(1)
        v1 = Vertex('2')
        v2 = Vertex()

        prev_id = id(v0)
        v0 += v1
        assert id(v0) == prev_id
        assert v0.neighbors == [v1]

        v2 += v0
        v2 += v1
        assert v2.neighbors == [v0, v1]

    def test___item__(self):
        v0 = Vertex(0)
        v1 = Vertex(1)
        v2 = Vertex(2)

        v0 += v1
        v0 += v2
        assert v0[0] == v1
        assert v0[1] == v2

        del v0[0]
        v0[0] = v1
        assert v0[0] == v1

    def test___str__(self):
        v = Vertex("name")
        assert v.__str__() == v.name

        v = Vertex()
        assert v.__str__() == str(id(v))

    def test_isConnected(self):
        v0 = Vertex(0)
        v1 = Vertex(1)

        v0 += v1
        assert v0.isConnected(v1) == True
        assert v1.isConnected(v0) == True

    def test__graph__iadd__(self):
        v0 = Vertex(0)
        v1 = Vertex(1)
        v2 = Vertex(2)

        g = Graph()

        prev_id = id(g)
        g += v0
        g += v1
        g += v2
        assert g.vertices == [v0, v1, v2]
        assert id(g) == prev_id
        for v in g.vertices:
            assert v.graph == g

    def test__graph__add__(self):
        v0 = Vertex(0)
        v1 = Vertex(1)
        v2 = Vertex(2)

        ids = [v0._id, v1._id, v2._id]
        print(ids)

        g = Graph()

        g = g + v0
        g = g + v1
        f = g + v2
        print(f._get_vertices_ids)
        assert f.vertices != [v0, v1, v2]
        for i, v in enumerate(f.vertices):
            assert v.name == i
            assert v.graph == f

        print(g._get_vertices_ids)
        assert g._get_vertices_ids == [0]

