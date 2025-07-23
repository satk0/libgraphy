import unittest
import pytest
from libgraphy import *

class TestGraphTraits(unittest.TestCase):

    def test_check_if_weighted_true(self):
        g: Graph = Graph()
        gt: GraphTraits = GraphTraits(g)
        for i in range(10):
            g += Vertex(i)

        for i in range(9):
            g += Edge(g.vertices[i], g.vertices[i+1], i)

        gt.check_if_weighted()
        assert gt.is_weighted is True

    def test_check_if_weighted_false(self):
        g: Graph = Graph()
        gt: GraphTraits = GraphTraits(g)
        for i in range(6):
            g += Vertex(i)

        for i in range(3):
            g += Edge(g.vertices[i], g.vertices[i+1])

        gt.check_if_weighted()
        assert gt.is_weighted is False

    def test_check_if_directional_false(self):
        g: Graph = Graph()
        gt: GraphTraits = GraphTraits(g)
        for i in range(5):
            g += Vertex(i)

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1])
            g += Edge(g.vertices[i+1], g.vertices[i])

        gt.check_if_directional()
        assert gt.is_directional is False

    def test_check_if_directional_true(self):
        g: Graph = Graph()
        gt: GraphTraits = GraphTraits(g)
        for i in range(5):
            g += Vertex(i)

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1], 2)
        g += Edge(g.vertices[3], g.vertices[2])

        gt.check_if_directional()
        assert gt.is_directional is True

    def test_check_if_directional_true_value(self):
        g: Graph = Graph()
        gt: GraphTraits = GraphTraits(g)
        for i in range(5):
            g += Vertex(i)

        for i in range(4):
            g += Edge(g.vertices[i], g.vertices[i+1])
            g += Edge(g.vertices[i+1], g.vertices[i], 2)

        gt.check_if_directional()
        assert gt.is_directional is True

    def test_check_if_grid_true(self):
        g: Graph = Graph()
        gt: GraphTraits = GraphTraits(g)
        for i in range(8):
            g += Vertex(i)

        for i in range(7):
            g += Edge(g.vertices[i], g.vertices[i+1])
            g += Edge(g.vertices[i+1], g.vertices[i])

        gt.check_if_grid()
        assert gt.is_grid is True

    def test_check_if_grid_false(self):
        g: Graph = Graph()
        gt: GraphTraits = GraphTraits(g)
        for i in range(8):
            g += Vertex(i)

        for i in range(6):
            g += Edge(g.vertices[i], g.vertices[i+1])

        g += Edge(g.vertices[4], g.vertices[3], 2)

        gt.check_if_grid()
        assert gt.is_grid is False
