from __future__ import annotations

__all__ = ["Vertex"]

from typing import Optional, Self, Any, Generator, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph

from .edge import Edge
from .exception import LibgraphyError

from copy import deepcopy

class Vertex:

    def __init__(self, name: Any = "", value: Any = 0, graph: Optional[Graph] = None) -> None:
        self.name: Any = name
        self.neighbors: list[Vertex] = []
        self.adjacent_edges: list[Edge] = [] # Distances to the neighbors
        self.value: int = value
        self.graph: Optional[Graph] = graph

    def isConnected(self, vertex: Vertex) -> bool:
        """Checks if self is connected to vertex"""
        return vertex in self.neighbors

    def __str__(self) -> str:
        return str(self.name)

    def __iter__(self) -> Generator[Vertex]:
        yield from self.neighbors

    # assign and add a neighbor to the current vertex (+= sign)
    def __iadd__(self, vertex: Vertex) -> Self:
        if not self.isConnected(vertex):
            self.neighbors.append(vertex)
        return self

    # add a neighbor to the current vertex (+ sign)
    def __add__(self, vertex: Vertex) -> Vertex:
        v: Vertex = self.copy()
        v.neighbors = [* self.neighbors]
        v.adjacent_edges = [* self.adjacent_edges]
        v += vertex
        return v

    def copy(self) -> Vertex:
        return Vertex(self.name, self.value, self.graph)

    # get i-th adjacency of the current vertex
    def __getitem__(self, key: int) -> Vertex:
        return self.neighbors[key]

    # change i-th adjacency of the current vertex
    def __setitem__(self, key: int, value: Self) -> None:
        self.neighbors[key] = value

    # delete i-th adjacency of the current vertex
    def __delitem__(self, key: int) -> None:
        del self.neighbors[key]

    # ********** Graph **********

    def _graph__iadd__(self, graph: Graph) -> Graph:
        if self.graph is graph:
            raise LibgraphyError("Vertex already belongs to this graph")
        if self.graph is not None:
            raise LibgraphyError("Vertex already belongs to another graph")

        self.graph = graph

        for v in graph.vertices:
            if v.isConnected(self):
                graph += Edge(v, self, graph)
            if self.isConnected(v):
                graph += Edge(self, v, graph)

        if graph.vertices and graph.vertices[-1] is self:
            # Vertex already added by Edge class
            return graph

        graph.vertices.append(self)
        return graph

    def _graph__add__(self, graph: Graph) -> Graph:
        edges_len: int = len(graph.edges)

        graph += self
        g: Graph = deepcopy(graph)

        edges_added: int = len(g.edges) - edges_len

        # * Bringing self back *
        del graph.vertices[-1]
        for _ in range(edges_added):
            e: Edge = graph.edges[-1]
            del e.predecessor.adjacent_edges[-1]
            del graph.edges[-1]
        self.graph = None
        # **********************

        return g

    # ***************************

