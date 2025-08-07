from __future__ import annotations

__all__ = ["_Algorithm", "_AlgorithmFunction", "AlgorithmEnum"]

from typing import TYPE_CHECKING, Deque, Optional, Callable, Dict
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .graph import Graph
    from .edge import Edge

from enum import Enum
from .exception import LibgraphyError

from .path import Path

from collections import deque 

type _AlgorithmFunction = Callable[[Graph, Vertex, Vertex], Path]

INFINITY = float("inf")

class AlgorithmEnum(Enum):
    DIJKSTRA = 1
    BELLMANFORD = 2
    ASTAR = 2

class _Algorithm:
    @staticmethod
    def dijkstra(graph: Graph, start: Vertex, end: Vertex) -> Path:
        # Taken and tweaked form of the following code:
        # https://github.com/dmahugh/dijkstra-algorithm/blob/master/dijkstra_algorithm.py
        unvisited_vertices: list[Vertex] = [* graph.vertices]  # All vertices are initially unvisited

        # Dictionary of each vertex's distance from start
        distance_from_start: Dict[Vertex, float] = {
            vertex: (0 if vertex == start else INFINITY) for vertex in graph.vertices
        }

        # Visited edge to reach vertex
        previous_edge: Dict[Vertex, Optional[Edge]] = {vertex: None for vertex in graph.vertices}

        while unvisited_vertices:
            current_vertex: Vertex = min(
                    unvisited_vertices, key=lambda vertex: distance_from_start[vertex]
                )
            unvisited_vertices.remove(current_vertex)

            if distance_from_start[current_vertex] == INFINITY:
                break

            for e in current_vertex.adjacent_edges:
                s: Vertex = e.successor

                new_path: float = distance_from_start[current_vertex] + e.value
                if new_path < distance_from_start[s]:
                    distance_from_start[s] = new_path
                    previous_edge[s] = e

            if current_vertex == end:
                break # Visited the destination vertex, finish

        path: Path = Path(graph)
        queue: Deque = deque()
        current_vertex: Vertex = end

        pe: Optional[Edge] = previous_edge[current_vertex]
        while pe is not None:
            queue.appendleft(pe)
            current_vertex = pe.predecessor
            pe = previous_edge[current_vertex]

        path.edges = list(queue)
        path.value = distance_from_start[end]

        return path

    @staticmethod
    def bellman_ford(graph: Graph, start: Vertex, end: Vertex) -> Path:
    # https://gist.github.com/ngenator/6178728
        # Dictionary of each vertex's distance from start
        distance_from_start: Dict[Vertex, float] = {
            vertex: (0 if vertex == start else INFINITY) for vertex in graph.vertices
        }
        # Visited edge to reach vertex
        previous_edge: Dict[Vertex, Optional[Edge]] = {vertex: None for vertex in graph.vertices}

        for _ in range(len(graph.vertices) - 1):
            for e in graph.edges:
                p: Vertex = e.predecessor
                s: Vertex = e.successor

                if distance_from_start[p] == INFINITY:
                    continue

                new_path: float = distance_from_start[p] + e.value
                if new_path < distance_from_start[s]:
                    distance_from_start[s] = new_path
                    previous_edge[s] = e

        for e in graph.edges:
            p: Vertex = e.predecessor
            s: Vertex = e.successor

            new_path: float = distance_from_start[p] + e.value
            if new_path < distance_from_start[s] + e.value:
                raise LibgraphyError("Negative cycle found!")

        path: Path = Path(graph)
        queue: Deque = deque()
        current_vertex: Vertex = end

        pe: Optional[Edge] = previous_edge[current_vertex]
        while pe is not None:
            queue.appendleft(pe)
            current_vertex = pe.predecessor
            pe = previous_edge[current_vertex]

        path.edges = list(queue)
        path.value = distance_from_start[end]

        return path

    @staticmethod
    def a_star(graph: Graph, start: Vertex, end: Vertex, grid_level: int) -> Path:
        pass
