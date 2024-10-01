from __future__ import annotations

__all__ = ["Edge"]

from typing import Optional, Self, Any, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .graph import Graph

from copy import deepcopy

from .exception import LibgraphyError

class Edge:
    def __init__(self, precedessor: Vertex, successor: Vertex, value: Any = 1, graph: Optional[Graph] = None) -> None:
        self.predecessor: Vertex = precedessor
        self.successor: Vertex = successor
        self.value: Any = value
        self.graph: Optional[Graph] = graph

    def __imul__(self, scalar: int | float) -> Self:
        self.value *= scalar
        return self

    def __mul__(self, scalar: int | float) -> Edge:
        return Edge(self.predecessor, self.successor, self.value * scalar)

    def __rmul__(self, scalar: int | float) -> Edge:
        return self * scalar

    def copy(self) -> Edge:
        return Edge(self.predecessor, self.successor, self.value, self.graph)

    # ********** Graph **********

    # don't move this !!
    def _graph__iadd__(self, graph: Graph) -> Graph:
        # Don't change the order of errors !!
        for e in graph.edges:
            if e.successor is self.successor and e.predecessor is self.predecessor:
                raise LibgraphyError("Edge already exists")

        if self.graph is not None:
            raise LibgraphyError("Edge belongs to a different graph")
        if (self.predecessor.graph not in [None, graph]):
            raise LibgraphyError("Predecessor belongs to a different graph")
        if (self.successor.graph not in [None, graph]):
            raise LibgraphyError("Successor belongs to a different graph")

        if self.predecessor not in graph.vertices:
            graph.vertices.append(self.predecessor)

        if self.successor not in graph.vertices:
            graph.vertices.append(self.successor)

        self.predecessor.graph = graph
        self.successor.graph = graph

        if self.successor not in self.predecessor.neighbors:
            self.predecessor.neighbors.append(self.successor)

        self.predecessor.adjacent_edges.append(self)

        self.graph = graph
        graph.edges.append(self)
        return graph

    def _graph__add__(self, graph: Graph) -> Graph:
        vertices_len = len(graph.vertices)
        p_graph = self.predecessor.graph
        s_graph = self.predecessor.graph
        p_neighbors_len = len(self.predecessor.neighbors)

        graph += self
        g: Graph = deepcopy(graph)

        vertices_added = len(g.vertices) - vertices_len

        # Bringing graph back
        del graph.edges[-1]
        for _ in range(vertices_added):
            del graph.vertices[-1]

        # Bringing self back
        del self.predecessor.adjacent_edges[-1]
        self.graph = None
        self.predecessor.graph = p_graph
        self.successor.graph = s_graph
        if p_neighbors_len != len(self.predecessor.neighbors):
            del self.predecessor.neighbors[-1]
        # **********
        return g

    # ***************************

