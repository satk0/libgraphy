from __future__ import annotations

__all__ = ["_Algorithm", "_AlgorithmFunction"]

from typing import TYPE_CHECKING, Optional, Self, Callable, Dict, cast
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .graph import Graph
    from .edge import Edge
#    from .route import Route

from .route import Route

from collections import deque 

type _AlgorithmFunction = Callable[[Graph, Vertex, Vertex], Route]

INFINITY = float("inf")

class _Algorithm:
    @staticmethod
    def djikstra(graph: Graph, start: Vertex, end: Vertex) -> Route:
        print("djikstra algorithm")

        unvisited_vertices: list[Vertex] = [* graph.vertices]  # All vertices are initially unvisited.

        # Create a dictionary of each node's distance from start_node. We will
        # update each node's distance whenever we find a shorter path.
        distance_from_start: Dict[Vertex, float] = {
            vertex: (0 if vertex == start else INFINITY) for vertex in graph.vertices
        }

        # Initialize previous_node, the dictionary that maps each node to the
        # node it was visited from when the the shortest path to it was found.
        previous_edge: Dict[Vertex, Optional[Edge]] = {vertex: None for vertex in graph.vertices}

        while unvisited_vertices:
            current_vertex = min(
                    unvisited_vertices, key=lambda vertex: distance_from_start[vertex]
                )
            unvisited_vertices.remove(current_vertex)

            if distance_from_start[current_vertex] == INFINITY:
                break

            for a in current_vertex.adjacencies:
                if not a.edge: # Skip not connected adjacencies
                    continue

                new_path = distance_from_start[current_vertex] + a.edge.value
                if new_path < distance_from_start[a.vertex]:
                    distance_from_start[a.vertex] = new_path
                    previous_edge[a.vertex] = a.edge

            if current_vertex == end:
                break # we've visited the destination node, so we're done

        route = Route(graph)
        path = deque()
        current_vertex = end
        while previous_edge[current_vertex] is not None:
            pe: Edge = previous_edge[current_vertex]
            path.appendleft(pe)
            current_vertex = pe.predecessor

        route.edges = list(path)
        route.value = distance_from_start[end]

        return route

    @staticmethod
    def bellmanFord(graph: Graph, start: Vertex, end: Vertex) -> Route:
        print("Bellman-Ford algorithm")
        return Route(Graph())
