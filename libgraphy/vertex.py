from __future__ import annotations

__all__ = ["Vertex"]

from typing import Optional, Self, Any, Generator, TYPE_CHECKING
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph
    from .edge import Edge
    from .edgeset import EdgeSet
from .exception import LibgraphyError

from copy import deepcopy

class Vertex(object):
    def __init__(self, name: Any = "", value: Any = 0, graph: Optional[Graph] = None, x: Optional[int] = None, y: Optional[int] = None) -> None:
        self.name: Any = name
        self.out_neighbors: list[Vertex]|None = None
        self.in_neighbors: list[Vertex]|None = None
        self.In_edges: EdgeSet|None = None
        self.out_edges: EdgeSet|None = None
        self.value: Any = value
        self.graph: Optional[Graph] = graph
        self.x: Optional[int] = x
        self.y: Optional[int] = y

    def isConnected(self, vertex: Vertex) -> bool:
        """Checks if self is connected to vertex"""
        if self.out_neighbors is None:
            return False
        return vertex in self.out_neighbors
    
    def distanceTo(self, vertex: Vertex) -> Any:
        if vertex in self.out_neighbors:
            return self.out_neighbors[vertex].value
        else:
            return None

    def __str__(self) -> str:
        return str(self.name)

    def __iter__(self) -> Generator[Vertex]:
        yield from self.out_neighbors
        
    def __getattribute__(self, item):
        if item == "out_neighbors":
            if self.graph is None:
                raise LibgraphyError("Vertex does not belong to a graph and has no out_neighbors")
            if self.graph.edges[self] is not None:
                list = self.graph.edges[self].vertices
                list.remove(self)
                return list
            else:
                return None
        elif item == "out_edges":
            if self.graph is None:
                raise LibgraphyError("Vertex does not belong to a graph and has no out_edges")
            return self.graph.edges[self]
        if item == "in_neighbors":
            if self.graph is None:
                raise LibgraphyError("Vertex does not belong to a graph and has no in_neighbors")
            if self.graph.edges[self] is not None:
                list = self.graph.edges.end_at(self).vertices
                list.remove(self)
                return list
            else:
                return None
        elif item == "in_edges":
            if self.graph is None:
                raise LibgraphyError("Vertex does not belong to a graph and has no in_edges")
            return self.graph.edges.end_at(self)
        else:
            return super().__getattribute__(item)

    def __getattr__(self, item):
        if item == "neighbors":
            return self.out_neighbors + self.in_neighbors

    def __gt__(self, successor: Vertex|list[Vertex]) -> Edge|EdgeSet:
        from .edge import Edge
        if isinstance(successor, Vertex):
            return Edge(self, successor)
        elif isinstance(successor, list):
            set = EdgeSet()
            for v in successor:
                set += Edge(self, v)
            return set
        raise LibgraphyError(f"Unsupported argument type for 'successor': {type(successor)} supplied")

    def __lt__(self, predecessor: Vertex|list[Vertex]) -> Edge|EdgeSet:
        from .edge import Edge
        if isinstance(predecessor, Vertex):
            return Edge(predecessor, self)
        elif isinstance(predecessor, list):
            set = EdgeSet()
            for v in predecessor:
                set += Edge(v, self)
            return set
        raise LibgraphyError(f"Unsupported argument type for 'predecessor': {type(predecessor)} supplied")

    def __sub__(self, other: Vertex|list[Vertex]) -> EdgeSet:
        from .edge import Edge
        from .edgeset import EdgeSet
        set = EdgeSet()
        if isinstance(other, Vertex):
            set += Edge(self, other)
            set += Edge(other, self)
            return set
        elif isinstance(other, list):
            for v in other:
                set += Edge(self, v)
                set += Edge(v, self)
            return set
        raise LibgraphyError(f"Unsupported argument type for 'other': {type(other)} supplied")

    # assign and add a neighbor to the current vertex (+= sign)
    def __iadd__(self, vertex: Vertex) -> Self:
        if self.isConnected(vertex):
            raise LibgraphyError("Vertices already connected")
        if vertex.graph is not None and vertex.graph is not self.graph:
            raise LibgraphyError("Vertex to be added belongs to a different graph")

        g = self.graph
        if g:
            g._create_edge(self, vertex)

        return self

    # get i-th adjacency of the current vertex
    def __getitem__(self, key: int|Vertex) -> Vertex|Any|None:
        if isinstance(key, int):
            if key in self.out_neighbors:
                return self.out_neighbors[key]
        elif isinstance(key, Vertex):
            if key in self.out_edges:
                return self.out_edges[key]
        else:
            raise LibgraphyError(f"key needs to be either of int or Vertex type, {type(key)} supplied")
        return None
        
    # change i-th adjacency of the current vertex
    def __setitem__(self, key: int|Vertex, value: Any) -> None:
        item = self[key]
        if item is None:
            raise LibgraphyError(f"'{key}' not found in '{self.name}' neighbors")
        if isinstance(key, int) and isinstance(value, Vertex):
            self.graph.edges.remove(self.graph.edges[self][key])
            self += value
        else:
            item = value
        
    # delete i-th adjacency of the current vertex
    def __delitem__(self, key: int|Vertex) -> None:
        if isinstance(key, Vertex):
            self.graph.edges.remove(self.graph.edges[self][key])
        elif isinstance(key, int):
            edge = self.out_edges[self.out_neighbors[key]]
            self.graph.edges.remove(edge)

    # ********** Graph **********

    def _graph__iadd__(self, g: Graph) -> Graph:
        if self.graph is not None and self.graph is not g:
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
            del e.predecessor.out_edges[-1]
            del graph.edges[-1]
        self.graph = None
        # **********************

        return g

    # ***************************

