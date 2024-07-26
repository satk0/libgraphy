import pytest

from ..graph import Vertex, Edge, Graph


class TestGraph:
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

        del v1[0]
        v1[0] = v2

        assert v1.neighbors == [v2]

    def test_edge_mult(self):
        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 10)
        e1 *= 10

        assert e1.value == 100

        e2 = e1 * 10

        assert e2.value == 1000 
        assert e1 != e2

    def test_graph_vertex_add(self):
        v1 = Vertex(1)
        v2 = Vertex(2)

        g = Graph()

        g += v1
        g += v2

        assert g.vertices == [v1, v2]
        assert g[0] == v1
        assert g[0].graph == g

        del g[0]
        assert g[0] == v2

    def test_graph_edge_add(self):
        v1 = Vertex(1)
        v2 = Vertex(2)

        e = Edge(v1, v2, 10)

        g = Graph()

        g += v1
        g += v2

        g += e

        assert g.edges == [e]
        assert e.graph == g
        assert e.predecessor.neighbors == [e.successor]
        assert e.successor.neighbors == [e.predecessor]
