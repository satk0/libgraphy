import unittest

from _pytest.monkeypatch import MonkeyPatch
import pytest

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

