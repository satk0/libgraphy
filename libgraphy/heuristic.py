__all__ = ["Heuristic", "ManhattanDistance", "HexagonalManhattanDistance", "ChebyshevDistance"]

from typing import TYPE_CHECKING
# if TYPE_CHECKING:
from .vertex import Vertex
from .graph import Graph

INFINITY = float("inf")

class Heuristic:
    def evaluate(self, v1: Vertex, v2: Vertex, g: Graph):
        for e in g.edges:
            if e.predecessor == v1 and e.successor == v2:
                return e.value
        return INFINITY

class ManhattanDistance(Heuristic):
    def evaluate(self, v1: Vertex, v2: Vertex, g: Graph):
        if None in [v1.x, v1.y, v2.x, v2.y]:
            return INFINITY
        return abs(v1.x - v2.x) + abs(v1.y - v2.y)

def _sign(x):
    return (x > 0) - (x < 0)

class HexagonalManhattanDistance(Heuristic):
    def evaluate(self, v1: Vertex, v2: Vertex, g: Graph) -> int | float:
        if None in [v1.x, v1.y, v2.x, v2.y]:
            return INFINITY

        dx = abs(v2.x - v1.x)
        dy = abs(v2.y - v1.y)

        if (_sign(dx) == _sign(dy)):
            return max(dx, dy)
        else:
            return dx + dy

class ChebyshevDistance(Heuristic):
    def evaluate(self, v1: Vertex, v2: Vertex, g: Graph):
        if None in [v1.x, v1.y, v2.x, v2.y]:
            return INFINITY

        return max(abs(v2.x - v1.x), abs(v2.y - v1.y))
