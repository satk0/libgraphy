import unittest
import pytest
from libgraphy import *
from libgraphy.utils import _DebugGraphviz
from .utils import create_test_graph

class TestPath(unittest.TestCase):

    def test__getitem__(self):
        p = Path(Graph())
        p.edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]

        e1 = p[1]
        assert e1.predecessor.name == '2' and e1.successor.name == '3' \
                and e1.value == 3.4

        e3 = p[3]
        assert e3.predecessor.name == '4' and e3.successor.name == '5' \
                and e3.value == 1.4

    def test__imul__(self):
        g = Graph()
        p = Path(g)
        edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]
        p.edges = edges 
        prev_val = p.value

        p *= 9.7

        for i in range(len(p.edges)):
            e = edges[i]
            re = p.edges[i]
            assert re.predecessor.name == e.predecessor.name
            assert re.successor.name == e.successor.name
            assert re.value == 9.7 * e.value
        assert p.value == 9.7 * prev_val
        assert p.graph is g

    def test__mul__(self):
        g = Graph()
        p = Path(g)
        p.edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]

        for e in p.edges:
            p.value += e.value

        np = 3.24 * p

        for i in range(len(np.edges)):
            npe = np.edges[i]
            pe = p.edges[i]
            assert npe.predecessor.name == pe.predecessor.name
            assert npe.successor.name == pe.successor.name
            assert npe.value == 3.24 * pe.value

        assert np.value == 3.24 * p.value
        assert p.graph is g
        assert np.graph is not g

    def test__draw_graph(self):
        EXPECTED_GRAPHVIZ_SOURCE = "digraph G {\n\tv0 [label=s color=green fontcolor=darkgreen]\n\tv1 [label=t color=green fontcolor=darkgreen]\n\tv2 [label=x color=green fontcolor=darkgreen]\n\tv3 [label=y color=green fontcolor=darkgreen]\n\tv4 [label=z]\n\tv0 -> v3 [label=5 color=green fontcolor=darkgreen]\n\tv3 -> v1 [label=3 color=green fontcolor=darkgreen]\n\tv1 -> v2 [label=1 color=green fontcolor=darkgreen]\n\tv0 -> v1 [label=10]\n\tv1 -> v3 [label=2]\n\tv3 -> v2 [label=9]\n\tv2 -> v4 [label=4]\n\tv4 -> v2 [label=6]\n\tv4 -> v0 [label=7]\n\tv3 -> v4 [label=2]\n}\n"

        g = create_test_graph()
        s, x = g.vertices[0], g.vertices[2]
        path: Path = g.find_path(s, x, algorithm = AlgorithmEnum.DIJKSTRA)

        dbg = _DebugGraphviz()
        path._repr_svg_(dbg = dbg)
        assert dbg.source == EXPECTED_GRAPHVIZ_SOURCE
