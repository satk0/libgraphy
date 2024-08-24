from __future__ import annotations

__all__ = ["Route"]

from typing import TYPE_CHECKING, Self
if TYPE_CHECKING: # pragma: no cover
    from .edge import Edge
    from .graph import Graph

class Route:
    def __init__(self, graph: Graph) -> None:
        self.graph: Graph = graph

        self.edges: list[Edge] = []
        self.value: int | float = 0

    # get i-th edge
    def __getitem__(self, key: int) -> Edge:
        return self.edges[key]

    def __imul__(self, scalar: int | float) -> Self:
        self.edges = [Edge(e.predecessor, e.successor, e.value * scalar, e.graph) for e in self.edges]
        return self

    def __mul__(self, scalar: int | float) -> Route:
        r = Route(self.graph)
        r *= scalar
        return r

    def __rmul__(self, scalar: int | float) -> Route:
        return self * scalar

