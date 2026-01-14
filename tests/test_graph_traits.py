import unittest
import pytest
from libgraphy import *
from .utils import grid_level4_graph, grid_level6_graph, grid_level8_graph

class TestGraphTraits(unittest.TestCase):

    def test_check_if_weighted_true(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(10):
            g += Vertex(i)

        for i in range(9):
            g += Edge(g.vertices[i], g.vertices[i+1], i)

        gt.check_if_weighted()
        assert gt.is_weighted is True

    def test_check_if_weighted_false(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        for i in range(3):
            g += Edge(g.vertices[i], g.vertices[i+1])

        gt.check_if_weighted()
        assert gt.is_weighted is False

    def test_check_if_directional_false(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(5):
            g += Vertex(i)

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1])
            g += Edge(g.vertices[i+1], g.vertices[i])

        gt.check_if_directional()
        assert gt.is_directional is False

    def test_check_if_directional_true(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(5):
            g += Vertex(i)

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1], 2)
        g += Edge(g.vertices[3], g.vertices[2])

        gt.check_if_directional()
        assert gt.is_directional is True

    def test_check_if_directional_true_value(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(5):
            g += Vertex(i)

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1])
            g += Edge(g.vertices[i+1], g.vertices[i], 2)

        gt.check_if_directional()
        assert gt.is_directional is True

    def test_check_if_grid_true(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(8):
            g += Vertex(i)

        for i in range(7):
            g += Edge(g.vertices[i], g.vertices[i+1])
            g += Edge(g.vertices[i+1], g.vertices[i])

        gt.check_if_grid()
        assert gt.is_grid is True

    def test_check_if_grid_false(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(8):
            g += Vertex(i)

        for i in range(6):
            g += Edge(g.vertices[i], g.vertices[i+1])

        g += Edge(g.vertices[4], g.vertices[3], 2)

        gt.check_if_grid()
        assert gt.is_grid is False

    def test_get_grid_level4(self):
        g: Graph = grid_level4_graph()
        gt: Graph.Traits = Graph.Traits(g)

        gt.check_if_grid()
        gt.get_grid_level()
        assert gt.is_grid is True and gt.grid_level is 4

    def test_get_grid_level6(self):
        g: Graph = grid_level6_graph()
        gt: Graph.Traits = Graph.Traits(g)

        gt.check_if_grid()
        gt.get_grid_level()
        assert gt.is_grid is True and gt.grid_level is 6

    def test_get_grid_level_error(self):
        g: Graph = grid_level4_graph()
        gt: Graph.Traits = Graph.Traits(g)

        with pytest.raises(LibgraphyError):
            gt.get_grid_level() # Error: gridness should be checked first

    def test_get_grid_level_not_grid(self):
        g: Graph = Graph()
        g += Edge("0", "1")
        gt: Graph.Traits = Graph.Traits(g)

        gt.check_if_grid()
        gt.get_grid_level()
        assert gt.is_grid is False and gt.grid_level is None

    def test_get_grid_level8(self):
        g: Graph = grid_level8_graph()
        gt: Graph.Traits = Graph.Traits(g)

        gt.check_if_grid()
        gt.get_grid_level()
        assert gt.is_grid is True and gt.grid_level is 8

    def test_check_if_has_cycles_false(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        for i in range(5):
            g += Edge(g.vertices[i], g.vertices[i+1])

        gt.check_if_has_cycles()
        assert gt.has_cycles is False

    def test_check_if_has_cycles_true(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        for i in range(5):
            g += Edge(g.vertices[i], g.vertices[i+1])
        g += Edge(g.vertices[-1], g.vertices[3])

        gt.check_if_has_cycles()
        assert gt.has_cycles is True

    def test_check_if_full_true(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(4):
            g += Vertex(i)

        visited = set()
        for v in g.vertices:
            for nv in g.vertices:
                if nv in visited or nv is v:
                    continue
                g += Edge(v, nv)
                g += Edge(nv, v)
            visited.add(v)

        gt.check_if_full()
        assert gt.is_full is True

    def test_check_if_full_false(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        for i in range(5):
            g += Edge(g.vertices[i], g.vertices[i+1])
            g += Edge(g.vertices[i+1], g.vertices[i])

        gt.check_if_full()
        assert gt.is_full is False

    def test_check_if_empty_true(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        gt.check_if_empty()
        assert gt.is_empty is True

    def test_check_if_empty_false(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        g += Edge(g.vertices[0], g.vertices[3])

        gt.check_if_empty()
        assert gt.is_empty is False

    def test_check_if_negative_edges_false(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        for i in range(5):
            g += Edge(g.vertices[i], g.vertices[i+1], i)

        gt.check_if_negative_edges()
        assert gt.has_negative_edges is False

    def test_check_if_negative_edges_true(self):
        g: Graph = Graph()
        gt: Graph.Traits = Graph.Traits(g)
        for i in range(6):
            g += Vertex(i)

        for i in range(5):
            g += Edge(g.vertices[i], g.vertices[i+1], i)

        g += Edge(g.vertices[3], g.vertices[0], -3)

        gt.check_if_negative_edges()
        assert gt.has_negative_edges is True

    def test_traits(self):
        g: Graph = grid_level6_graph()
        g += Edge(g.vertices[0], g.vertices[-1], -4)
        gt: Graph.Traits = Graph.Traits.traits(g)

        assert gt.is_weighted is True
        assert gt.has_negative_edges is True
        assert gt.is_directional is True
        assert gt.is_grid is False
        assert gt.grid_level is None
        assert gt.has_cycles is True
        assert gt.is_full is False
        assert gt.is_empty is False

