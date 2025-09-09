import unittest
import pytest

from libgraphy import *
from .utils import create_test_graph, create_grid_graph, create_hexagonal_flat_graph, create_octogonal_graph


INFINITY = float("inf")

class TestHeuristic(unittest.TestCase):
    def test_heuristic_evaluate(self):
        g = create_test_graph()
        end = g.vertices[-1]
        h = Heuristic()

        for v in g.vertices:
            expected_val = INFINITY
            for e in v.adjacent_edges:
                if e.successor == end:
                    expected_val = e.value

            value = h.evaluate(v, end, g)
            assert expected_val == value

    def test_manhattan_distance_evaluate(self):
        # o - o - t - o
        # o - o - o - o
        # o - o - o - o
        # o - o - o - o
        # o - o - o - o
        # s - o - o - o

        g: Graph = create_grid_graph(6, 4)

        s = g.vertices[0]
        t = g.vertices[5 * 4 + 2]

        h: ManhattanDistance = ManhattanDistance()

        assert h.evaluate(s, t, g) is 7

    def test_hexagonal_manhattan_distance_evaluate(self):
        g: Graph = create_hexagonal_flat_graph(3, 4)

        s = g.vertices[0]
        t = g.vertices[-1]

        h: HexagonalManhattanDistance = HexagonalManhattanDistance()

        assert h.evaluate(s, t, g) is 3

    def test_chebyshev_distance_evaluate(self):
        g: Graph = create_octogonal_graph(5, 6)

        s = g.vertices[0]
        t = g.vertices[-3]

        h: ChebyshevDistance = ChebyshevDistance()

        assert h.evaluate(s, t, g) is 4

