import unittest
import pytest

from libgraphy import Vertex, Graph
from libgraphy.exception import LibgraphyError

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
        assert v.__str__() == ""

    def test_isConnected(self):
        v0 = Vertex(0)
        v1 = Vertex(1)

        v0 += v1
        assert v0.isConnected(v1) == True
        assert v1.isConnected(v0) == False

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

    def test__graph__iadd__neighbors(self):
        v0 = Vertex("a")
        vertices = ["v2","v3","v4","v5"]
        for v in vertices:
            v0 += Vertex(v)

        g = Graph()
        g += v0
        for n in v0:
            g += n

        for i, e in enumerate(g.edges):
            assert e.predecessor is v0 and e.successor is v0.neighbors[i]
            # a -> v2, a -> v3, ...

        # reverse order
        v0 = Vertex("a")
        vertices = [Vertex() for _ in range(4)]
        for v in vertices:
            v += v0

        g = Graph()
        for v in vertices:
            g += v

        g += v0

        print(g.edges)
        for i, e in enumerate(g.edges):
            assert e.predecessor is vertices[i] and e.successor is v0
            # v2 -> a, v3 -> a, ...

    def test__graph__iadd__exception(self):
        v0 = Vertex()

        g0 = Graph()
        g1 = Graph()

        g0 += v0
        with pytest.raises(LibgraphyError) as e:
            g1 += v0
        assert str(e.value) == "Vertex already belongs to another graph"

        v1 = Vertex()
        g1 += v1
        with pytest.raises(LibgraphyError) as e:
            g1 += v1
        print(e.value)
        assert str(e.value) == "Vertex already belongs to this graph"

    def test__graph__add__(self):
        v0 = Vertex(0)
        v1 = Vertex(1)
        v2 = Vertex(2)

        g = Graph()

        g += v0
        f = g + v1
        f = f + v2
        assert f.vertices != [v0, v1, v2]
        for i, v in enumerate(f.vertices):
            assert v.name == i
            assert v.value == 0
            assert v.graph == f

    def test__graph__add__exception(self):
        v0 = Vertex()

        g0 = Graph()
        g1 = Graph()

        g0 += v0
        with pytest.raises(LibgraphyError) as e:
            g1 = g1 + v0
        assert str(e.value) == "Vertex already belongs to another graph"

        v1 = Vertex()
        g1 += v1
        with pytest.raises(LibgraphyError) as e:
            g1 = g1 + v1
        print(e.value)
        assert str(e.value) == "Vertex already belongs to this graph"

