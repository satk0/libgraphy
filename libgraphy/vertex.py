from __future__ import annotations

__all__ = ["Vertex"]

from typing import Self, Any, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph

from copy import deepcopy

class Vertex:
    __id = 0

    def __init__(self, name: Any = "", value: Any = 0, graph: Graph | None = None) -> None:
        self.name: Any = name
        self.neighbors: list[Self] | list = []
        self.value: int = value
        self.graph: Graph | None = graph

        # to uniquely identify vertex
        self._id = Vertex.__id
        Vertex.__id += 1

    def isConnected(self, vertex: Self) -> bool:
        return vertex in self.neighbors or self in vertex.neighbors

    def __str__(self) -> str:
        if self.name:
            return str(self.name)
        else:
            return str(self._id)

    # assign and add a neighbor to the current vertex (+= sign)
    def __iadd__(self, vertex: Self) -> Self:
        self.neighbors.append(vertex)
        return self

    # add a neighbor to the current vertex (+ sign)
    def __add__(self, vertex: Self) -> Vertex:
        v: Vertex = self.copy()
        v.neighbors = [* self.neighbors]
        v.neighbors.append(vertex)
        return v

    def copy(self) -> Vertex:
        return Vertex(self.name, self.value, self.graph)

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
        g: Graph = graph.copy()
        g.vertices = [Vertex(v.name, v.value, g) for v in g.vertices]

        v = self.copy()
        v.graph = g
        g.vertices.append(v)
        return g

    # ***************************

