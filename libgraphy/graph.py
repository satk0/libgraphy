from __future__ import annotations

__all__ = ["Graph", "AlgorithmEnum"]

from typing import TYPE_CHECKING, Self
if TYPE_CHECKING: # pragma: no cover
    from .vertex import Vertex
    from .edge import Edge

from enum import Enum
from .algorithm import _Algorithm, _AlgorithmFunction

try:
    import graphviz as gv
except ImportError:
    gv = None

try:
    import IPython.display as ipds
except ImportError:
    ipds = None

from copy import deepcopy

class AlgorithmEnum(Enum): 
    DJIKSTRA = 1
    BELLMANFORD = 2

class Graph:

    __algorithms = {
            AlgorithmEnum.DJIKSTRA: _Algorithm.djikstra,
            AlgorithmEnum.BELLMANFORD: _Algorithm.bellmanFord
    }

    def __init__(self, incidence_matrix = None) -> None:
        self.vertices: list[Vertex] = []
        self.edges: list[Edge] = []

    # get i-th vertex of the graph
    def __getitem__(self, key: int) -> Vertex:
        return self.vertices[key]

    # change i-th vertex in the graph
    def __setitem__(self, key: int, value: Vertex) -> None:
        self.vertices[key] = value

    # delete i-th vertex of the graph
    def __delitem__(self, key: int) -> None:
        del self.vertices[key]

    def __iadd__(self, element: Vertex | Edge) -> Graph:
        return element._graph__iadd__(self)

    def __add__(self, element: Vertex | Edge) -> Graph:
        return element._graph__add__(self)

    def __imul__(self, scalar: int | float) -> Self:
        self.edges = [Edge(e.predecessor, e.successor, e.value * scalar, self) for e in self.edges]
        return self

    def __mul__(self, scalar: int | float) -> Graph:
        tmp_edges = self.edges

        self *= scalar
        g = deepcopy(self)

        self.edges = tmp_edges

        return g

    def __repr__(self) -> str:
        repr_txt = "Vertices:\n"

        repr_txt += '{'
        for v in self.vertices:
            repr_txt += f'{str(v)}, '

        repr_txt = repr_txt.removesuffix(', ')
        repr_txt += '}\n'

        repr_txt += "Edges:\n"
        for e in self.edges:
            repr_txt += f"w_{str(e.predecessor)}{str(e.successor)} = {e.value}; "

        return repr_txt

    # This class is used only for tests
    class _DebugGraphviz():
        source: str = ""

    # dbg is passed as a object reference
    def _repr_svg_(self, dbg: _DebugGraphviz | None = None):
        if not ipds:
            raise ImportError("No IPython installed")

        if not gv:
            raise ImportError("No GraphViz installed")

        g = gv.Digraph('G')

        for v in self.vertices:
            g.node(str(v))

        for e in self.edges:
            g.edge(str(e.predecessor), str(e.successor), label=str(e.value))

        if dbg:
            dbg.source = g.source

        ipds.display_svg(g)

    def _repr_png_(self, dbg: _DebugGraphviz | None = None):
        if not ipds:
            raise ImportError("No IPython installed")

        if not gv:
            raise ImportError("No GraphViz installed")

        g = gv.Digraph('G')

        for v in self.vertices:
            g.node(str(v))

        for e in self.edges:
            g.edge(str(e.predecessor), str(e.successor), label=str(e.value))

        if dbg:
            dbg.source = g.source

        ipds.display_png(g)

    def _repr_latex_(self) -> str:
        latex_txt = r"$$\begin{gathered}" + '\n'

        latex_txt += "Vertices:"
        latex_txt += " \\\\ \n"

        latex_txt += r"\{"
        for v in self.vertices:
            latex_txt += f'{str(v)},'
        latex_txt = latex_txt.removesuffix(',')
        latex_txt += r"\} \\\\" + "\n"

        latex_txt += "Edges:"
        latex_txt += " \\\\ \n"

        for e in self.edges:
            latex_txt += r"w_{%s%s} = %s \\" % (str(e.predecessor), str(e.successor), e.value) + '\n'

        latex_txt += r"\end{gathered}$$"

        return latex_txt


    def copy(self) -> Graph:
        g = Graph()
        g.vertices = [* self.vertices]
        g.edges = [* self.edges]

        return g

    def findPath(self, algorithm: AlgorithmEnum, start: Vertex, end: Vertex):
        path_algorithm: _AlgorithmFunction = self.__algorithms[algorithm]
        path_algorithm(self, start, end)
        return

