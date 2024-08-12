from __future__ import annotations

__all__ = ["Edge"]

from typing import Self, Any, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .graph import Graph

from copy import deepcopy

class Edge:
    __id = 0

    def __init__(self, precedessor: Vertex, successor: Vertex, value: Any = 0, graph: Graph | None = None) -> None:
        self.predecessor: Vertex = precedessor
        self.successor: Vertex = successor
        self.value: Any = value
        self.graph: Graph | None = graph

        # to uniquely identify vertex
        self._id = Edge.__id
        Edge.__id += 1

    def __imul__(self, scalar: int | float) -> Self:
        self.value *= scalar
        return self

    def __mul__(self, scalar: int | float) -> Edge:
        return Edge(self.predecessor, self.successor, self.value * scalar)

    def __rmul__(self, scalar: int | float) -> Edge:
        return self.__mul__(scalar)

    def copy(self) -> Edge:
        return Edge(self.predecessor, self.successor, self.value, self.graph)

    # don't move this !!
    def _graph__iadd__(self, graph: Graph) -> Graph:
        self.predecessor.graph = graph
        self.successor.graph = graph

        self.predecessor += self.successor
        self.successor += self.predecessor

        self.graph = graph
        graph.edges.append(self)
        return graph

    def _graph__add__(self, graph: Graph) -> Graph:
        g: Graph = graph.copy()
        g.edges = [Edge(e.predecessor, e.successor, e.value, g) for e in g.edges]

        e = self.copy()

        e.predecessor = e.predecessor.copy()
        e.successor = e.successor.copy()

        e.predecessor.graph = g
        e.successor.graph = g

        e.predecessor += e.successor
        e.successor += e.predecessor

        e.graph = g

        g.edges.append(e)
        return g


