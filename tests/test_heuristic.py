import unittest
import pytest

from libgraphy import *
from .utils import create_test_graph


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





