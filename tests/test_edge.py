import unittest
import pytest

from libgraphy import Vertex, Edge, Graph
from libgraphy.exception import LibgraphyError

class TestEdge(unittest.TestCase):
    def test___mult__(self):
        e = Edge(Vertex(), Vertex())

        prev_edge = [e.predecessor, e.successor]
        res = e * 10
        assert res.value == 10
        assert [res.predecessor, res.successor] == prev_edge

        # __rmult__
        prev_edge = [e.predecessor, e.successor]
        res = 10 * e
        assert res.value == 10
        assert [res.predecessor, res.successor] == prev_edge

    def test___imult__(self):
        e = Edge(Vertex(), Vertex(), 10)

        prev_id = id(e)
        prev_edge = [e.predecessor, e.successor]
        e *= 10
        assert id(e) == prev_id
        assert e.value == 100
        assert [e.predecessor, e.successor] == prev_edge

    def test_copy(self):
        e = Edge(Vertex(), Vertex(), 34.23)

        ecp = e.copy()

        assert ecp.predecessor is e.predecessor
        assert ecp.successor is e.successor
        assert ecp.value is e.value

    def test__graph__iadd__(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        v4 = Vertex(4)

        e1 = Edge(v1, v2, 10)
        e2 = Edge(v2, v3, 1.3)
        e3 = Edge(v1, v4)

        correct_edges = [[1, 2, 10], [2, 3, 1.3], [1, 4, 1]]

        g = Graph()

        g += v1
        g += v2

        g += e1
        g += e2
        g += e3

        assert g.vertices == [v1, v2, v3, v4]
        assert g.edges == [e1, e2, e3]
        for i, e in enumerate(g.edges):
            p = e.predecessor
            s = e.successor
            assert p in g.vertices and s in g.vertices
            assert p.name == correct_edges[i][0] and s.name == correct_edges[i][1]
            assert e.value == correct_edges[i][2]
            assert p.isConnected(s) and not s.isConnected(p)
            assert p.graph is g and s.graph is g and e.graph is g

    def test__graph__iadd__exceptions(self):
        v0 = Vertex(1)
        v1 = Vertex(2)

        edge0 = Edge(v0, v1, 10)
        edge1 = Edge(v1, v0, -1)
        edge2 = Edge(Vertex(), Vertex(), 0)

        g0 = Graph()
        g1 = Graph()

        g0 += v0
        with pytest.raises(LibgraphyError) as e:
            g1 += edge0
        assert str(e.value) == "Predecessor belongs to a different graph"

        with pytest.raises(LibgraphyError) as e:
            g1 += edge1
        assert str(e.value) == "Successor belongs to a different graph"

        g0 += edge0
        with pytest.raises(LibgraphyError) as e:
            g0 += edge0
        assert str(e.value) == "Edge already exists"

        g0 += edge2
        with pytest.raises(LibgraphyError) as e:
            g1 += edge2
        assert str(e.value) == "Edge belongs to a different graph"

    def test__graph__add__(self):
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex(3)
        v4 = Vertex(4)

        e1 = Edge(v1, v2, 10)
        e2 = Edge(v3, v4, -1.4)

        correct_edges = [[1, 2, 10], [3, 4, -1.4]]

        g = Graph()

        g += v1
        g += v2

        f = g + e1
        f = f + e2

        assert f.vertices != [v1, v2, v3, v4]
        assert f.edges != [e1, e2]
        assert len(f.edges) == 2
        assert len(f.vertices) == 4
        for i, e in enumerate(f.edges):
            p = e.predecessor
            s = e.successor
            assert p in f.vertices and s in f.vertices
            assert p.name == correct_edges[i][0] and s.name == correct_edges[i][1]
            assert e.value == correct_edges[i][2]
            assert p.isConnected(s) and not s.isConnected(p)
            assert p.graph is f and s.graph is f and e.graph is f

        # ensure nothing has been changed
        assert g.edges == []
        assert g.vertices == [v1, v2]

        assert e1.graph is None and e2.graph is None

        assert v1.neighbors == v3.neighbors == []
        assert v1.adjacent_edges == v3.adjacent_edges == []
        assert v1.graph is g and v2.graph is g
        assert v3.graph is None and v4.graph is None

    def test__graph__add__exceptions(self):
        v0 = Vertex(1)
        v1 = Vertex(2)

        edge0 = Edge(v0, v1, 10)
        edge1 = Edge(v1, v0, -1)
        edge2 = Edge(Vertex(), Vertex(), 0)

        g0 = Graph()
        g1 = Graph()

        g0 += v0
        with pytest.raises(LibgraphyError) as e:
            g1 = g1 + edge0
        assert str(e.value) == "Predecessor belongs to a different graph"

        with pytest.raises(LibgraphyError) as e:
            g1 = g1 + edge1
        assert str(e.value) == "Successor belongs to a different graph"

        g0 += edge0
        with pytest.raises(LibgraphyError) as e:
            g0 = g0 + edge0
        assert str(e.value) == "Edge already exists"

        g0 += edge2
        with pytest.raises(LibgraphyError) as e:
            g1 = g1 + edge2
        assert str(e.value) == "Edge belongs to a different graph"

