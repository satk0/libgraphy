import unittest
import pytest
from libgraphy import *
from libgraphy.utils import _DebugGraphviz
#from libgraphy.exception import LibgraphyError

class TestRoute(unittest.TestCase):

    def test__getitem__(self):
        r = Route(Graph())
        r.edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]

        e1 = r[1]
        assert e1.predecessor.name == '2' and e1.successor.name == '3' \
                and e1.value == 3.4

        e3 = r[3]
        assert e3.predecessor.name == '4' and e3.successor.name == '5' \
                and e3.value == 1.4

    def test__imul__(self):
        g = Graph()
        r = Route(g)
        edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]
        r.edges = edges 
        r *= 9.7

        for i in range(len(r.edges)):
            e = edges[i]
            re = r.edges[i]
            assert re.predecessor.name == e.predecessor.name
            assert re.successor.name == e.successor.name
            assert re.value == 9.7 * e.value
        assert r.graph is g

    def test__mul__(self):
        g = Graph()
        r = Route(g)
        r.edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]

        nr = 3.24 * r

        for i in range(len(nr.edges)):
            nre = nr.edges[i]
            re = r.edges[i]
            assert nre.predecessor.name == re.predecessor.name
            assert nre.successor.name == re.successor.name
            assert nre.value == 3.24 * re.value

        assert r.graph is g
        assert nr.graph is not g

    @staticmethod
    def create_graph():
        # same graph as for algorithm
        vertices = [Vertex(l) for l in "stxyz"]
        s, t, x, y, z = vertices

        edges = [Edge(s, y, 5), Edge(y, t, 3), Edge(t, x),
                Edge(s, t, 10), Edge(t, y, 2), Edge(y, x, 9),
                 Edge(x, z, 4), Edge(z, x, 6), Edge(z, s, 7),
                 Edge(y, z, 2)]

        g = Graph()
        for v in vertices:
            g += v

        for e in edges:
            g += e

        return g

    def test__draw_graph(self):
        g = TestRoute.create_graph()

        s, x = g.vertices[0], g.vertices[2]

        route: Route = g.findPath(AlgorithmEnum.DJIKSTRA, s, x)
        EXPECTED_GRAPHVIZ_SOURCE = "digraph G {\n\tv0 [label=s color=green fontcolor=darkgreen]\n\tv1 [label=t color=green fontcolor=darkgreen]\n\tv2 [label=x color=green fontcolor=darkgreen]\n\tv3 [label=y color=green fontcolor=darkgreen]\n\tv4 [label=z]\n\tv0 -> v3 [label=5 color=green fontcolor=darkgreen]\n\tv3 -> v1 [label=3 color=green fontcolor=darkgreen]\n\tv1 -> v2 [label=1 color=green fontcolor=darkgreen]\n\tv0 -> v1 [label=10]\n\tv1 -> v3 [label=2]\n\tv3 -> v2 [label=9]\n\tv2 -> v4 [label=4]\n\tv4 -> v2 [label=6]\n\tv4 -> v0 [label=7]\n\tv3 -> v4 [label=2]\n}\n"

        dbg = _DebugGraphviz()
        route._repr_svg_(dbg = dbg)

        assert dbg.source == EXPECTED_GRAPHVIZ_SOURCE
