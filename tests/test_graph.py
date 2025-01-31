import unittest

from _pytest.monkeypatch import MonkeyPatch
import pytest

from csv import reader
import tempfile

from libgraphy import Vertex, Edge, Graph

import sys


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

    def test__graph__item__(self):
        v0 = Vertex(1)
        v2 = Vertex(2)

        g = Graph()

        g += v0
        g += v2

        v = g[0]
        del g[0]
        g[0] = v

        assert g.vertices == [v0]

    @staticmethod
    def repr_init_graph():
        v1 = Vertex(1)
        v2 = Vertex(2)
        v3 = Vertex('c')

        e1 = Edge(v1, v2, 2)
        e2 = Edge(v3, v2, -3)
        e3 = Edge(v1, v3, 3)
        e4 = Edge(v3, v1, 'aa')

        g = Graph()

        g += v1
        g += v2
        g += v3

        g += e1
        g += e2
        g += e3
        g += e4

        return g

    def test_graph_repr(self):
        g = self.repr_init_graph()

        # use pytest --pdb
        # and then in shell: repr(g)
        # to fix this in future
        REPR_RES = "Vertices:\n{1, 2, c}\nEdges:\nw_12 = 2; w_c2 = -3; w_1c = 3; w_c1 = aa; "

        assert repr(g) == REPR_RES

    def test_graph_latex_repr(self):
        g = self.repr_init_graph()

        # use pytest --pdb
        # and then in shell: g._repr_latex_()
        # to fix this in future
        LATEX_REPR_RES = "$$\\begin{gathered}\nVertices: \\\\ \n\\{1,2,c\\} \\\\\\\\\nEdges: \\\\ \nw_{12} = 2 \\\\\nw_{c2} = -3 \\\\\nw_{1c} = 3 \\\\\nw_{c1} = aa \\\\\n\\end{gathered}$$"

        assert g._repr_latex_() == LATEX_REPR_RES

    def test_graph_png_repr(self):
        g = self.repr_init_graph()

        GRAPHVIZ_SOURCE = "digraph G {\n\tv0 [label=1]\n\tv1 [label=2]\n\tv2 [label=c]\n\tv0 -> v1 [label=2]\n\tv2 -> v1 [label=-3]\n\tv0 -> v2 [label=3]\n\tv2 -> v0 [label=aa]\n}\n"

        dbg = Graph._DebugGraphviz()
        g._repr_png_(dbg = dbg)

        assert dbg.source == GRAPHVIZ_SOURCE

    def test_graph_svg_repr(self):
        g = self.repr_init_graph()

        GRAPHVIZ_SOURCE = "digraph G {\n\tv0 [label=1]\n\tv1 [label=2]\n\tv2 [label=c]\n\tv0 -> v1 [label=2]\n\tv2 -> v1 [label=-3]\n\tv0 -> v2 [label=3]\n\tv2 -> v0 [label=aa]\n}\n"

        dbg = Graph._DebugGraphviz()
        g._repr_svg_(dbg = dbg)

        assert dbg.source == GRAPHVIZ_SOURCE

    def test_graph_graphviz_import_error(self):
        gv = sys.modules['graphviz']
        self.monkeypatch.setitem(sys.modules, 'graphviz', None)
        self.monkeypatch.delitem(sys.modules, 'libgraphy')
        self.monkeypatch.delitem(sys.modules, 'libgraphy.graph')

        from libgraphy import Vertex, Edge, Graph

        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 2)

        g = Graph()

        g += v1
        g += v2

        g += e1

        with pytest.raises(ImportError):
            g._repr_png_()
        with pytest.raises(ImportError):
            g._repr_svg_()


        self.monkeypatch.setitem(sys.modules, 'graphviz', gv)

    def test_graph_ipython_import_error(self):
        ipd = sys.modules['IPython']
        self.monkeypatch.setitem(sys.modules, 'IPython', None)
        self.monkeypatch.delitem(sys.modules, 'libgraphy')
        self.monkeypatch.delitem(sys.modules, 'libgraphy.graph')

        from libgraphy import Vertex, Edge, Graph

        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 2)

        g = Graph()

        g += v1
        g += v2

        g += e1

        with pytest.raises(ImportError):
            g._repr_png_()
        with pytest.raises(ImportError):
            g._repr_svg_()

        self.monkeypatch.setitem(sys.modules, 'IPython', ipd)

    def test__imul__(self):
        g = self.repr_init_graph()
        edges = g.edges

        g *= 4

        for i in range(len(g.edges)):
            e = edges[i]
            ge = g.edges[i]
            assert ge.value == 4 * e.value
            assert e.graph is ge.graph is g

    def test_graph__iadd__(self):
        g = Graph()

        for i in range(10):
            g += Edge("g", "g", i)

        h = Graph()

        for i in range(10):
            h += Edge("h", "h", i * (-1))

        combined_edges = g.edges + h.edges
        g += h

        for i in range(len(combined_edges)):
            ce = combined_edges[i]
            ge = g.edges[i]
            assert ce.predecessor is ge.predecessor \
                    and ce.successor is ge.successor \
                    and ce.value == ge.value \
                    and ge.graph is g

    def test_graph__add__(self):
        g = Graph()

        for i in range(10):
            g += Edge("g", "g", i)

        h = Graph()

        for i in range(10):
            h += Edge("h", "h", i * (-1))

        combined_edges = g.edges + h.edges
        f = g + h

        for i in range(len(combined_edges)):
            ce = combined_edges[i]
            fe = f.edges[i]
            assert ce.predecessor is not fe.predecessor \
                    and ce.predecessor.name == fe.predecessor.name \
                    and ce.successor is not fe.successor \
                    and ce.successor.name == fe.successor.name \
                    and ce.value == fe.value \
                    and fe.graph is f

    def test__mul__(self):
        g = self.repr_init_graph()
        h = 4 * g

        for i in range(len(h.edges)):
            ge = g.edges[i]
            he = h.edges[i]
            assert he.value == 4 * ge.value
            assert he.graph is not g and ge.graph is g

    def test_find_vertex_by_name(self):
        g = Graph()
        for i in range(10):
            g += Vertex(str(i))

        expected_vertex = g.vertices[5]
        vertex = g.find_vertex_by_name("5")

        assert vertex is expected_vertex

    def test_grap(self):
        g = Graph()
        for i in range(10):
            g += Vertex(str(i))

        expected_vertex = g.vertices[5]
        vertex = g.find_vertex_by_name("5")

        assert vertex is expected_vertex

    # change to JSON
    def test_write_to_csv(self):
        g = self.repr_init_graph()

        with tempfile.TemporaryDirectory() as tmpdirname:
            loc = tmpdirname + "/graph.csv"
            Graph.write_to_csv(g, loc)
            with open(loc, 'r') as csvfile:
                csvreader = reader(csvfile)
                i = 0
                for row in csvreader:
                    assert row[0] == str(g.edges[i].predecessor.name) and \
                        row[1] == str(g.edges[i].successor.name) and \
                        row[2] == str(g.edges[i].value)
                    i += 1

    # change to JSON
    def test_read_from_csv(self):
        loc = "./tests/fixtures/graph.csv"
        expected_graph = Graph.read_from_csv(loc)
        g = self.repr_init_graph()

        assert len(g.edges) == len(expected_graph.edges)
        for i in range(len(g.edges)):
            edge = g.edges[i]
            expected_edge = expected_graph.edges[i]

            assert expected_edge.predecessor.name == edge.predecessor.name and \
                expected_edge.successor.name == edge.successor.name and \
                expected_edge.value == edge.value

# 401
