import unittest

import pytest

import tempfile

try:
    import networkx as nx
    nx_found = True
except ImportError:
    nx_found = False

try:
    from scipy.sparse import csr_matrix
    scipy_found = True
except ImportError:
    scipy_found = False

from libgraphy import Vertex, Edge, Graph, LibgraphyError
from libgraphy.utils import _DebugGraphviz
from .utils import assert_compare_graph_values, create_test_graph

import sys
import jsonpickle

import filecmp

class TestGraph(unittest.TestCase):
    # def setUp(self):
    #     self.monkeypatch = MonkeyPatch()

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

        dbg = _DebugGraphviz()
        g._repr_png_(dbg = dbg)
        # To fix GRAPHVIZ_SOURCE:
        # print(repr(dbg.source))

        assert dbg.source == GRAPHVIZ_SOURCE

    def test_graph_svg_repr(self):
        g = self.repr_init_graph()

        GRAPHVIZ_SOURCE = "digraph G {\n\tv0 [label=1]\n\tv1 [label=2]\n\tv2 [label=c]\n\tv0 -> v1 [label=2]\n\tv2 -> v1 [label=-3]\n\tv0 -> v2 [label=3]\n\tv2 -> v0 [label=aa]\n}\n"

        dbg = _DebugGraphviz()
        g._repr_svg_(dbg = dbg)

        assert dbg.source == GRAPHVIZ_SOURCE

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

    def test_write(self):
        g = TestGraph.repr_init_graph()

        expected = Graph.to_json(g)
        s = Graph.write(g)

        assert s == expected

    def test_read(self):
        g = TestGraph.repr_init_graph()

        s = Graph.to_json(g)
        ng = Graph.read(s)

        assert_compare_graph_values(g, ng)

    def test_to_json(self):
        g = TestGraph.repr_init_graph()

        expected = jsonpickle.encode(g, indent=1)
        s = Graph.to_json(g)

        assert s == expected

    def test_from_json(self):
        g = TestGraph.repr_init_graph()

        s = Graph.to_json(g)
        ng = Graph.from_json(s)

        assert_compare_graph_values(g, ng)

    def test_from_json_dupped(self):
        g = Graph()
        for i in range(10):
            g += Edge("g", "g", i)

        s = Graph.to_json(g)
        ng = Graph.from_json(s)

        assert_compare_graph_values(g, ng)

    def test_write_to_json(self):
        g = self.repr_init_graph()
        with tempfile.TemporaryDirectory() as tmpdirname:
            loc = tmpdirname + "/graph.json"
            Graph.write_to_json_file(g, loc)
            assert filecmp.cmp('./tests/fixtures/expected_graph.json', loc, shallow=False)

    def test_read_from_json(self):
        expected_graph = create_test_graph()
        graph = Graph.read_from_json_file('./tests/fixtures/graph_to_read_from.json')

        assert_compare_graph_values(graph, expected_graph)

    def test_to_networkx_repeated(self):
        if not nx_found:
            return

        g: Graph = Graph()

        for _ in range(5):
            g += Vertex(1)

        for i in range(len(g.vertices) - 1):
            g += Edge(g.vertices[i], g.vertices[i+1], i)

        nxg: nx.DiGraph = Graph.to_networkx(g)
        assert "{}".format(nxg.edges.data()) == "[(1, '1_0', {'weight': 0}), ('1_0', '1_1', {'weight': 1}), ('1_1', '1_2', {'weight': 2}), ('1_2', '1_3', {'weight': 3})]"

    def test_to_networkx_normal(self):
        if not nx_found:
            return

        g: Graph = self.repr_init_graph()
        nxg: nx.DiGraph = Graph.to_networkx(g)

        assert "{}".format(nxg.edges.data()) == "[(1, 2, {'weight': 2}), (1, 'c', {'weight': 3}), ('c', 2, {'weight': -3}), ('c', 1, {'weight': 'aa'})]"

    def test_from_networkx(self):
        if not nx_found:
            return

        nxg: nx.DiGraph = nx.DiGraph()

        for i in range(10):
            nxg.add_edge(i, i+1, weight = i)

        g: Graph = Graph.from_networkx(nxg)

        # To check run: print(repr(str(g)))
        assert str(g) == 'Vertices:\n{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10}\nEdges:\nw_01 = 0; w_12 = 1; w_23 = 2; w_34 = 3; w_45 = 4; w_56 = 5; w_67 = 6; w_78 = 7; w_89 = 8; w_910 = 9; '

    def test_to_csgraph(self):
        if not scipy_found:
            return

        g: Graph = Graph()
        for i in range(5):
            g += Vertex(str(i))

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1], i+1)
        g += Edge(g.vertices[-1], g.vertices[0], 0.64)

        csg: csr_matrix = Graph.to_csgraph(g)
        print(repr(str(csg.toarray())))

        assert str(csg.toarray()) == "[[0.   1.   0.   0.   0.  ]\n [0.   0.   2.   0.   0.  ]\n [0.   0.   0.   3.   0.  ]\n [0.   0.   0.   0.   4.  ]\n [0.64 0.   0.   0.   0.  ]]"

    def test_to_csgraph_error(self):
        if not scipy_found:
            return

        g: Graph = Graph()
        for i in range(5):
            g += Vertex(str(i))

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1], str(i+1))

        with pytest.raises(LibgraphyError):
            csg: csr_matrix = Graph.to_csgraph(g) # Error: not using int or float

    def test_from_csgraph(self):
        adjacency_matrix = [
            [0, 1, 2, 0],
            [0, 0, 0, 1],
            [2, 0, 0, 3],
            [0, 0, 0, 0]]

        csg: csr_matrix = csr_matrix(adjacency_matrix)

        g: Graph = Graph.from_csgraph(csg)

        assert str(g) == "Vertices:\n{0, 1, 2, 3}\nEdges:\nw_01 = 1; w_02 = 2; w_13 = 1; w_20 = 2; w_23 = 3; "


# TODO: FIX THIS SOMEDAY:
'''

    def test_graph_graphviz_import_error(self):
        # gv = sys.modules['graphviz']
        # # self.monkeypatch.setitem(sys.modules, 'graphviz', None)
        # self.monkeypatch.delitem(sys.modules, 'graphviz')
        # self.monkeypatch.delitem(sys.modules, 'libgraphy')
        # self.monkeypatch.delitem(sys.modules, 'libgraphy.graph')
        with mock.patch.dict(sys.modules, {'graphviz':None}):

            import graphviz

            v1 = Vertex(1)
            v2 = Vertex(2)

            e1 = Edge(v1, v2, 2)

            g = Graph()

            g += v1
            g += v2

            g += e1

            # g._repr_png_()
            # g._repr_svg_()
            # assert 1 == 0

            with pytest.raises(ImportError):
                g._repr_png_()
            with pytest.raises(ImportError):
                g._repr_svg_()


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
'''

