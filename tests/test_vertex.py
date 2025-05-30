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
        assert v0.adjacent_edges == []
        assert v1.neighbors == []
        assert v1.adjacent_edges == []
        assert id(v0) != prev_id

        v3 = v0 + v2
        n0 = v3.neighbors[0]
        assert n0.name == v1.name and n0.value == v1.value

        n1 = v3.neighbors[1]
        assert n1.name == v2.name and n0.value == v2.value
        assert v3.adjacent_edges == []
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
        assert v0.adjacent_edges == []

        v2 += v0
        v2 += v1

        assert v2.neighbors == [v0, v1]
        assert v2.adjacent_edges == []

    def test___iadd__errors1(self):
        v1 = Vertex()
        v2 = Vertex()

        g = Graph()
        g += v2

        with pytest.raises(LibgraphyError):
            v1 += v2

    def test___iadd__errors2(self):
        v0 = Vertex(1)
        v1 = Vertex('2')

        v0 += v1

        with pytest.raises(LibgraphyError):
            v0 += v1

        v2 = Vertex(3)
        g1 = Graph()
        g2 = Graph()

        g1 += v1
        g2 += v2

        with pytest.raises(LibgraphyError):
            v1 += v2

    def test___iadd__graph_edges_1(self):
        v1 = Vertex("a")
        vertices_names = ["v2", "v3", "v4", "v5"]
        vertices = [Vertex(name) for name in vertices_names]
        v2, v3, v4, v5 = vertices
        expected_edges = ((v1, v2), (v1, v3), (v1, v4), (v1, v5))

        g = Graph()
        g += v1
        for v in vertices:
            v1 += v

        assert g.vertices == [v1] + vertices
        for i, e in enumerate(expected_edges):
            p = g.edges[i].predecessor
            s = g.edges[i].successor
            assert e[0] is p and e[1] is s
            assert g.edges[i].value == 1

    def test___iadd__graph_edges_2(self):
        v1 = Vertex("a")
        vertices_names = ["v2", "v3", "v4", "v5"]
        vertices = [Vertex(name) for name in vertices_names]
        v2, v3, v4, v5 = vertices
        expected_edges = ((v1, v2), (v1, v3), (v1, v4), (v1, v5))

        g = Graph()
        g += v1
        for v in vertices:
            g += v
        for v in vertices:
            v1 += v

        for i, e in enumerate(expected_edges):
            p = g.edges[i].predecessor
            s = g.edges[i].successor
            assert e[0] == p and e[1] == s

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

        assert len(g.edges) == len(vertices)
        for i, e in enumerate(g.edges):
            assert e.predecessor is v0 and e.successor is v0[i]
            assert not e.successor.isConnected(e.predecessor)
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

        assert len(g.edges) == len(vertices)
        for i, e in enumerate(g.edges):
            assert e.predecessor is vertices[i] and e.successor is v0
            assert not e.successor.isConnected(e.predecessor)
            # v2 -> a, v3 -> a, ...

    def test__graph__iadd__neighbors_double(self):
        v0 = Vertex("a")
        v1 = Vertex("b")

        v0 += v1
        v1 += v0

        g = Graph()

        g += v0
        g += v1

        edges = [[v0, v1], [v1, v0]]

        assert len(g.edges) == len(edges)
        for i, e in enumerate(g.edges):
            assert e.predecessor is edges[i][0] and e.successor is edges[i][1]

    def test__graph__iadd__exception(self):
        v0 = Vertex()

        g0 = Graph()
        g1 = Graph()

        g0 += v0
        with pytest.raises(LibgraphyError):
            g1 += v0

        v1 = Vertex()
        g1 += v1
        with pytest.raises(LibgraphyError):
            g1 += v1

    def test__graph__add__(self):
        v0 = Vertex(0)
        v1 = Vertex(1)
        v2 = Vertex(2)

        g = Graph()

        g += v0
        f = g + v1
        f = f + v2
        # TODO: add function to compare graphs
        assert f.vertices != [v0, v1, v2]
        for i, v in enumerate(f.vertices):
            assert v.name == i
            assert v.value == 0
            assert v.graph == f

        # make sure nothing has been changed on the original graph
        assert g.vertices == [v0]

    def test__graph__add__neighbors(self):
        v0 = Vertex("a")
        vertices = ["v2","v3","v4","v5"]
        for v in vertices:
            v0 += Vertex(v)

        pre_neighbors = [* v0.neighbors]

        g = Graph()
        g += v0
        f = g + v0[0] # v2
        for i in range(1, len(v0.neighbors)):
            f = f + v0[i] # v3, v4, v5

        # only a -> v2 because with each "+" operation graph is deepcopied
        assert len(f.edges) == 1

        e = f.edges[-1]
        p = e.predecessor
        s = e.successor
        assert p in f.vertices and s in f.vertices
        assert p.isConnected(s) and not s.isConnected(p)
        assert p.name == "a" and s.name == "v2"
        assert p.graph is f and s.graph is f
        assert e.graph is f

        # Should not change original vertices
        assert v0.neighbors == pre_neighbors
        assert v0.adjacent_edges == [] # should not add any edge
        for i, n in enumerate(v0):
            assert n.name == pre_neighbors[i].name
            assert n.value == pre_neighbors[i].value
            assert n.graph is None

        # ***** reverse order *****

        v0 = Vertex("a")
        v1 = Vertex("b")
        vertices = [Vertex(i) for i in range(4)]
        for v in vertices:
            v += v0
            v += v1

        pre_neighbors = [* v0.neighbors]

        g = Graph()
        for v in vertices:
            g += v

        f = g + v0
        f += v1

        assert len(f.edges) == 4
        for i, e in enumerate(f.edges):
            p = e.predecessor
            s = e.successor
            assert p in f.vertices and s in f.vertices
            assert p.name == vertices[i].name and s.name == v0.name
            assert p.isConnected(s) and not s.isConnected(p)
            assert p.graph is f and s.graph is f
            assert e.graph is f

        # Should not change original vertices
        assert v0.neighbors == pre_neighbors
        assert v0.adjacent_edges == [] # should not add any edge

    def test__graph__add__neighbors_double(self):
        v0 = Vertex("a")
        v1 = Vertex("b")

        v0 += v1
        v1 += v0

        g = Graph()

        g += v0
        f = g + v1

        edges = [["a", "b"], ["b", "a"]]

        assert len(f.vertices) == len(edges)
        for i, e in enumerate(f.edges):
            p = e.predecessor
            s = e.successor
            assert p.name is edges[i][0] and s.name is edges[i][1]
            assert s.isConnected(p) and p.isConnected(s)
            assert p in f.vertices and s in f.vertices
            assert p.graph is f and s.graph is f and e.graph is f

    def test__graph__add__exception(self):
        v0 = Vertex()

        g0 = Graph()
        g1 = Graph()

        g0 += v0
        with pytest.raises(LibgraphyError):
            g1 = g1 + v0

        v1 = Vertex()
        g1 += v1
        with pytest.raises(LibgraphyError):
            g1 = g1 + v1

