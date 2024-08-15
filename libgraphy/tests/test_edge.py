import unittest
import pytest

from libgraphy import Vertex, Edge, Graph

class TestEdge(unittest.TestCase):
    def test___mult__(self):
        e = Edge(Vertex(), Vertex(), 10)

        prev_edge = [e.predecessor, e.successor]
        res = e * 10
        assert res.value == 100
        assert [res.predecessor, res.successor] == prev_edge

        # __rmult__
        prev_edge = [e.predecessor, e.successor]
        res = 10 * e
        assert res.value == 100
        assert [res.predecessor, res.successor] == prev_edge

    def test___imult__(self):
        e = Edge(Vertex(), Vertex(), 10)

        prev_id = id(e)
        prev_edge = [e.predecessor, e.successor]
        e *= 10
        assert id(e) == prev_id
        assert e.value == 100
        assert [e.predecessor, e.successor] == prev_edge

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
        assert e1.predecessor.graph == g
        assert e1.successor.graph == g
        assert e1.successor.neighbors == []

    def test__graph__add__(self):
        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 10)
        e2 = Edge(v2, v1, -10)

        correct_edges = [[1, 2, 10], [2, 1, -10]]

        g = Graph()

        g += v1
        g += v2
        g += e1

        f = g + e2

        assert f.edges != [e1, e2]
        for i, e in enumerate(f.edges):
            assert e.predecessor.name == correct_edges[i][0]
            assert e.successor.name == correct_edges[i][1]
            assert e.value == correct_edges[i][2]

        # ensure nothing has been changed
        assert g.edges == [e1]
        assert g.vertices == [v1, v2]

