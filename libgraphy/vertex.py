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
        self.value: Any = value
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
        if self.isConnected(vertex):
            raise LibgraphyError("Vertices already connected")
        if vertex.graph is not None and vertex.graph is not self.graph:
            raise LibgraphyError("Vertex to be added belongs to a different graph")

        g = self.graph
        if g:
            g._create_edge(self, vertex)

        self.neighbors.append(vertex)
        return self

    # add a neighbor to the current vertex (+ sign)
    def __add__(self, vertex: Vertex) -> Vertex:
        v: Vertex = deepcopy(self)
        v += vertex
        return v

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

    def _graph__iadd__(self, g: Graph) -> Graph:
        if self.graph is g:
            raise LibgraphyError("Vertex already belongs to this graph")
        if self.graph is not None:
            raise LibgraphyError("Vertex already belongs to another graph")

        g.vertices.append(self)
        self.graph = g

        for v in g.vertices:
            if v.isConnected(self):
                g._create_edge(v, self)
            if self.isConnected(v):
                g._create_edge(self, v)

        return g

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

