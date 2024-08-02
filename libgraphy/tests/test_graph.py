import unittest

from _pytest.monkeypatch import MonkeyPatch
import pytest

from ..graph import Vertex, Edge, Graph

import sys

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.monkeypatch = MonkeyPatch()

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
        REPR_RES = "Vertices:\n{1, 2, c}\nEdges:\nw_12 = 2w_c2 = -3w_1c = 3w_c1 = aa"

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

        GRAPHVIZ_SOURCE = "digraph G {\n\t1\n\t2\n\tc\n\t1 -> 2 [label=2]\n\tc -> 2 [label=-3]\n\t1 -> c [label=3]\n\tc -> 1 [label=aa]\n}\n"

        dbg = Graph._DebugGraphviz()
        g._repr_png_(dbg = dbg)

        assert dbg.source == GRAPHVIZ_SOURCE

    def test_graph_svg_repr(self):
        g = self.repr_init_graph()

        GRAPHVIZ_SOURCE = "digraph G {\n\t1\n\t2\n\tc\n\t1 -> 2 [label=2]\n\tc -> 2 [label=-3]\n\t1 -> c [label=3]\n\tc -> 1 [label=aa]\n}\n"

        dbg = Graph._DebugGraphviz()
        g._repr_svg_(dbg = dbg)

        assert dbg.source == GRAPHVIZ_SOURCE

    def test_graph_graphviz_import_error(self):
        gv = sys.modules['graphviz']
        self.monkeypatch.setitem(sys.modules, 'graphviz', None)
        self.monkeypatch.delitem(sys.modules, 'libgraphy')
        self.monkeypatch.delitem(sys.modules, 'libgraphy.graph')

        from ..graph import Vertex, Edge, Graph

        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 2)

        g = Graph()

        g += v1
        g += v2

        g += e1

        out_png = g._repr_png_()
        out_svg = g._repr_svg_()

        # comparing types suffices
        assert type(out_png) == type(ImportError())
        assert type(out_svg) == type(ImportError())

        self.monkeypatch.setitem(sys.modules, 'graphviz', gv)

    def test_graph_ipython_import_error(self):
        ipd = sys.modules['IPython']
        self.monkeypatch.setitem(sys.modules, 'IPython', None)
        self.monkeypatch.delitem(sys.modules, 'libgraphy')
        self.monkeypatch.delitem(sys.modules, 'libgraphy.graph')

        from ..graph import Vertex, Edge, Graph

        v1 = Vertex(1)
        v2 = Vertex(2)

        e1 = Edge(v1, v2, 2)

        g = Graph()

        g += v1
        g += v2

        g += e1

        out_png = g._repr_png_()
        out_svg = g._repr_svg_()

        assert type(out_png) == type(ImportError())
        assert type(out_svg) == type(ImportError())

        self.monkeypatch.setitem(sys.modules, 'IPython', ipd)

