from __future__ import annotations

__all__ = ["Vertex"]

from typing import Self, Any, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph

from copy import deepcopy

class Vertex:
    def __init__(self, name: Any = "", value: Any = 0, graph: Graph | None = None) -> None:
        self.name: Any = name
        self.neighbors: list[Self] | list = []
        self.value: int = value
        self.graph: Graph | None = graph

    def isConnected(self, vertex: Self) -> bool:
        return vertex in self.neighbors or self in vertex.neighbors

    def __str__(self) -> str:
        if self.name:
            return str(self.name)
        else:
            return str(id(self))

    # assign and add a neighbor to the current vertex (+= sign)
    def __iadd__(self, vertex: Self) -> Self:
        self.neighbors.append(vertex)
        return self

    # add a neighbor to the current vertex (+ sign)
    def __add__(self, vertex: Self) -> Vertex:
        v: Vertex = Vertex(self.name, self.value, self.graph)
        v.neighbors = [* self.neighbors]
        v.neighbors.append(vertex)
        return v

    # get i-th neighbor of the current vertex
    def __getitem__(self, key: int) -> Self:
        return self.neighbors[key]

    # change i-th neighbor of the current vertex
    def __setitem__(self, key: int, value: Self) -> None:
        self.neighbors[key] = value

    # delete i-th neighbor of the current vertex
    def __delitem__(self, key: int) -> None:
        del self.neighbors[key]

    # ********** Graph **********

    def _graph__iadd__(self, graph: Graph) -> Graph:
        self.graph = graph
        graph.vertices.append(self)
        return graph

    def _graph__add__(self, graph: Graph) -> Graph:
        g: Graph = deepcopy(graph)

        self.graph = g
        g.vertices.append(self)
        return g

    # ***************************

