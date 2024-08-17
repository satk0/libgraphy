from __future__ import annotations

__all__ = ["Edge"]

from typing import Self, Any, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .graph import Graph

from copy import deepcopy

from .exception import LibgraphyError

class Edge:
    def __init__(self, precedessor: Vertex, successor: Vertex, value: Any = 1, graph: Graph | None = None) -> None:
        self.predecessor: Vertex = precedessor
        self.successor: Vertex = successor
        self.value: Any = value
        self.graph: Graph | None = graph

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
        if (self.predecessor.graph not in [None, graph]):
            raise LibgraphyError("Predecessor belongs to a different graph")
        if (self.successor.graph not in [None, graph]):
            raise LibgraphyError("Successor belongs to a different graph")

        for e in graph.edges:
            if e.successor is self.successor and e.predecessor is self.predecessor:
                raise LibgraphyError("Edge already exists")

        if self.predecessor not in graph.vertices:
            graph.vertices.append(self.predecessor)

        if self.successor not in graph.vertices:
            graph.vertices.append(self.successor)

        self.predecessor.graph = graph
        self.successor.graph = graph

        # defines "self.successor" as neighbor
        self.predecessor += self.successor

        self.graph = graph
        graph.edges.append(self)
        return graph

    def _graph__add__(self, graph: Graph) -> Graph:
        if (self.predecessor.graph not in [None, graph]):
            raise LibgraphyError("Predecessor belongs to a different graph")
        if (self.successor.graph not in [None, graph]):
            raise LibgraphyError("Successor belongs to a different graph")

        for e in graph.edges:
            if e.successor is self.successor and e.predecessor is self.predecessor:
                raise LibgraphyError("Edge already exists")

        graph.edges.append(self)

        to_delete = 0
        if self.predecessor not in graph.vertices:
            graph.vertices.append(self.predecessor)
            to_delete += 1

        if self.successor not in graph.vertices:
            graph.vertices.append(self.successor)
            to_delete += 1

        g: Graph = deepcopy(graph)

        # Bring back
        del graph.edges[-1]
        for _ in range(to_delete):
            del graph.vertices[-1]
        # **********

        e = g.edges[-1]
        e.graph = g
        e.predecessor.graph = g
        e.successor.graph = g

        e.predecessor += e.successor

        return g

