from __future__ import annotations

__all__ = ["Vertex"]

from typing import Optional, Self, Any, Generator, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph

from .edge import Edge
from .exception import LibgraphyError

from copy import deepcopy

class Vertex:

    # Make it separate: "neighbours" and "adjacent_edges"
    class Adjacency:
        def __init__(self, vertex: Vertex, edge: Optional[Edge]) -> None:
            self.vertex: Vertex = vertex
            self.edge: Optional[Edge] = edge # Distance to the neighbor

    def __init__(self, name: Any = "", value: Any = 0, graph: Graph | None = None) -> None:
        self.name: Any = name
        self.adjacencies: list[Vertex.Adjacency] = []
        self.value: int = value
        self.graph: Optional[Graph] = graph

    def isConnected(self, vertex: Vertex) -> bool:
        """Checks if self is connected to vertex"""
        for a in self.adjacencies:
            if a.vertex is vertex:
                return True
        return False

    def __str__(self) -> str:
        return str(self.name)

    def __iter__(self) -> Generator[Vertex.Adjacency]:
        yield from self.adjacencies

    # assign and add a neighbor to the current vertex (+= sign)
    def __iadd__(self, vertex: Self) -> Self:
        if not self.isConnected(vertex):
            self.adjacencies.append(Vertex.Adjacency(vertex, None))
        return self

    # add a neighbor to the current vertex (+ sign)
    def __add__(self, vertex: Self) -> Vertex:
        v: Vertex = self.copy()
        v.adjacencies = [* self.adjacencies]
        v += vertex
        return v

    def copy(self) -> Vertex:
        return Vertex(self.name, self.value, self.graph)

    # get i-th adjacency of the current vertex
    def __getitem__(self, key: int) -> Vertex.Adjacency:
        return self.adjacencies[key]

    # change i-th adjacency of the current vertex
    def __setitem__(self, key: int, value: Self) -> None:
        self.adjacencies[key] = Vertex.Adjacency(value, None)

    # delete i-th adjacency of the current vertex
    def __delitem__(self, key: int) -> None:
        del self.adjacencies[key]

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
        edges_len = len(graph.edges)

        graph += self
        g: Graph = deepcopy(graph)

        edges_added = len(g.edges) - edges_len

        # Bringing self back
        del graph.vertices[-1]
        for _ in range(edges_added):
            del graph.edges[-1]
        self.graph = None
        # **********

        return g

    # ***************************

