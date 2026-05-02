from __future__ import annotations

__all__ = ["Edge", "_EdgeList"]

from typing import Optional, Self, Any, TYPE_CHECKING, override
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph

from .vertex import Vertex
from copy import deepcopy

from .exception import LibgraphyError
from .utils import EdgeOverrideMode
from random import randint

class Edge:
    def __init__(self, precedessor: Vertex | str, successor: Vertex | str, value: Any = 1, graph: Optional[Graph] = None) -> None:
        if isinstance(precedessor, Vertex):
            self.predecessor: Vertex = precedessor
        elif isinstance(precedessor, str):
            self.predecessor: Vertex = Vertex(precedessor)
        if isinstance(successor, Vertex):
            self.successor: Vertex = successor
        elif isinstance(successor, str):
            self.successor: Vertex = Vertex(successor)

        self.value: Any = value
        self.graph: Optional[Graph] = graph
        
        if self not in self.predecessor.adjacent_edges:
            self.predecessor.adjacent_edges.append(self)
        if self.successor not in self.predecessor.neighbors:
            self.predecessor.neighbors.append(self.successor)

    def __imul__(self, scalar: int | float) -> Self:
        self.value *= scalar
        return self

    def __mul__(self, scalar: int | float) -> Edge:
        return Edge(self.predecessor, self.successor, self.value * scalar)

    def __rmul__(self, scalar: int | float) -> Edge:
        return self * scalar
    
    def reverse(self, override: bool = False) -> Edge:
        # If reverse edge already in graph
        if self.graph is not None and self.graph.edges[(self.successor, self.predecessor)] is not None:
            if override:
                self.graph.edges.remove(self)
            else:
                raise LibgraphyError(f"Edge cannot be reversed, as reverse edge already exists in graph")
            
        # Remove from current predecessor
        self.predecessor.neighbors.remove(self.successor)
        self.predecessor.adjacent_edges.remove(self)
        
        # If successor already is connected to predecessor
        if self.predecessor in self.successor.neighbors:
            # Remove old edges
            all = self.successor.adjacent_edges
            endingAt = all.end_at(self.predecessor)
            all -= endingAt
        else:
            self.successor.neighbors.append(self.predecessor)
            
        # Add self to edges and swap direction
        self.successor.adjacent_edges.append(self)
        self.predecessor, self.successor = self.successor, self.predecessor
        
        # Return edge for chaining
        return self
        
    def randomize_direction(self) -> Edge:
        if randint(0, 1):
            if self.successor.isConnected(self.predecessor):
                self.value, self.successor[self.predecessor].value = self.successor[self.predecessor].value, self.value
            else:
                self.reverse()
        return self
    
    def make_undirected(self, mode: EdgeOverrideMode = EdgeOverrideMode.AVERAGE) -> _EdgeList:
        both_edges = _EdgeList()
        both_edges.append(self)
        
        # If reverse edge does not exist - create it
        if not self.successor.isConnected(self.predecessor):
            other_direction = Edge(self.successor, self.predecessor, self.value)
            if self.graph is not None:
                self.graph += other_direction
            both_edges.append(other_direction)
    
        # If reverse edge already exists - perform unification
        else:
            if mode == EdgeOverrideMode.EXCEPTION:
                raise LibgraphyError(f"Edge ({self.successor.name}->{self.predecessor.name}) already exists in graph")
            both_edges.append([e for e in self.successor.adjacent_edges if e.successor == self.predecessor][0])
            if mode != EdgeOverrideMode.IGNORE:
                if mode == EdgeOverrideMode.AVERAGE:
                    new_value = (float(self.predecessor[self.successor]) + float(self.successor[self.predecessor])) / 2
                elif mode == EdgeOverrideMode.MAXIMUM:
                    new_value = max(self.predecessor[self.successor], self.successor[self.predecessor])
                elif mode == EdgeOverrideMode.MINIMUM:
                    new_value = min(self.predecessor[self.successor], self.successor[self.predecessor])
                self.predecessor[self.successor] = new_value
                self.successor[self.predecessor] = new_value
    
        # Return the set of both edges
        return both_edges

    # ********** Graph **********

    # don't move this !!
    def _graph__iadd__(self, graph: Graph) -> Graph:
        # Don't change the order of errors !!
        for e in graph.edges:
            if e.successor is self.successor and e.predecessor is self.predecessor:
                raise LibgraphyError(f"Edge already exists ({e.predecessor}->{e.successor})")

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

class _EdgeList(list):
    def __init__(self, graph: Optional[Graph] = None) -> None:
        self.graph: Optional[Graph] = graph

    def start_at(self, start_vertex: Vertex) -> _EdgeList:
        startingAt = _EdgeList()
        startingAt.graph = start_vertex.graph
        for e in self:
            if e.predecessor == start_vertex:
                startingAt.append(e)
        return startingAt

    def end_at(self, end_vertex: Vertex) -> _EdgeList:
        endingAt = _EdgeList()
        endingAt.graph = end_vertex.graph
        for e in self:
            if e.successor == end_vertex:
                endingAt.append(e)
        return endingAt
    
    def reverse(self, override: bool = False):
        for e in self:
            e.reverse(override)

    @override
    def __getitem__(self, key: Any) -> Edge|None:
        if isinstance(key, tuple):
            for e in self:
                if e.predecessor == key[0] and e.successor == key[1]:
                    return e
            return None
        elif isinstance(key, Edge):
            for e in self:
                if e.predecessor == key.predecessor and e.successor == key.successor:
                    return e
            return None
        else:
            return super().__getitem__(key)
        
    @override
    def __setitem__(self, key: Any, value: Any) -> None:
        edge = self[key]
        if edge is not None:
            edge.value = value
        elif isinstance(key, tuple):
            self.append(Edge(key[0], key[1], value))
        elif isinstance(key, Edge):
            key.value = value
            self.append(key)
        else:
            super().__setitem__(key, value)
            
    def __isub__(self, edges: _EdgeList) -> _EdgeList:
        for e in edges:
            self.remove(e)
        return self

    def __sub__(self, edges: _EdgeList) -> _EdgeList:
        newList = deepcopy(self)
        newList -= edges
        return newList

    # ********** Graph **********

    # don't move this !!
    def _graph__iadd__(self, graph: Graph) -> Graph:
        for e in self:
            graph += e
        return graph

    def _graph__add__(self, graph: Graph) -> Graph:
        g: Graph = deepcopy(graph)
        g += self
        return g

    # ***************************