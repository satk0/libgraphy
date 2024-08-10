from __future__ import annotations

__all__ = ["Edge"]

from typing import Self, Any, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .graph import Graph

from copy import deepcopy

class Edge:
    def __init__(self, precedessor: Vertex, successor: Vertex, value: Any = 0) -> None:
        self.graph: Graph | None = None
        self.predecessor: Vertex = precedessor
        self.successor: Vertex = successor
        self.value: Any = value

    def __imul__(self, scalar: int | float) -> Self:
        self.value *= scalar
        return self

    def __mul__(self, scalar: int | float) -> Self:
        e: Self = deepcopy(self)
        e.value *= scalar
        return e


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
        g: Graph = deepcopy(graph)

        self.predecessor.graph = g
        self.successor.graph = g

        self.predecessor += self.successor
        self.successor += self.predecessor

        self.graph = g

        g.edges.append(self)
        return g

