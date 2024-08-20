from __future__ import annotations

__all__ = ["_Algorithm", "_AlgorithmFunction"]

from typing import TYPE_CHECKING, Self, Callable
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .graph import Graph

type _AlgorithmFunction = Callable[[Graph, Vertex, Vertex], None]

class _Algorithm:
    @staticmethod
    def djikstra(graph: Graph, start: Vertex, end: Vertex):
        print("djikstra algorithm")

    @staticmethod
    def bellmanFord(graph: Graph, start: Vertex, end: Vertex):
        print("Bellman-Ford algorithm")
