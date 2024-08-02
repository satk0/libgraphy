from typing import Dict, Any, Self
from copy import deepcopy
import sys

try:
    import graphviz as gv
except ImportError:
    gv = None

try:
    import IPython.display as ipds
except ImportError:
    ipds = None

from .decorators.multidispatch import multidispatch

class Vertex:
    def __init__(self, name: Any, value: Any = 0) -> None:
        self.graph: Graph | None = None
        self.name: Any = name
        self.neighbors: list[Self] =  []
        self.value: int = value

    def isConnected(self, vertex: Self) -> bool:
        return vertex in self.neighbors

    def __str__(self) -> str:
        return str(self.name)

    # assign and add a neighbor to the current vertex (+= sign)
    def __iadd__(self, vertex: Self) -> Self:
        self.neighbors.append(vertex)
        return self

    # add a neighbor to the current vertex (+ sign)
    def __add__(self, vertex: Self) -> Self:
        v: Self = deepcopy(self)
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


class Edge:
    def __init__(self, precedessor: Vertex, successor: Vertex, value: Any = 0) -> None:
        self.graph: Graph | None = None
        self.predecessor: Vertex = precedessor
        self.successor: Vertex = successor
        self.value: Any = value

    def __imul__(self, scalar: int | float) -> Self:
        self.value *= scalar
        return self

    def __mul__(self, scalar: int | float) -> Self:
        e: Self = deepcopy(self)
        e.value *= scalar
        return e


class Graph:
    def __init__(self) -> None:
        self.vertices: list[Vertex] = []
        self.edges: list[Edge] = []

    # get i-th vertex of the graph
    def __getitem__(self, key: int) -> Vertex:
        return self.vertices[key]

    # change i-th vertex in the graph
    def __setitem__(self, key: int, value: Vertex) -> None:
        neighbors = self.vertices[key].neighbors
        self.vertices[key] = value
        self.vertices[key].neighbors = neighbors

    # delete i-th vertex of the graph
    def __delitem__(self, key: int) -> None:
        del self.vertices[key]

    # assign and add a vertex to the graph (+= sign)
    @multidispatch(Vertex)
    def __iadd__(self, vertex: Vertex) -> Self:
        vertex.graph = self
        self.vertices.append(vertex)
        return self

    @multidispatch(Edge)
    def __iadd__(self, edge: Edge) -> Self:
        edge.predecessor.graph = self
        edge.successor.graph = self

        edge.predecessor += edge.successor
        edge.successor += edge.predecessor

        edge.graph = self
        self.edges.append(edge)
        return self

    # add a neighbor to the current vertex (+ sign)
    @multidispatch(Vertex)
    def __add__(self, vertex: Vertex) -> Self:
        g: Self = deepcopy(self)

        vertex.graph = g
        g.vertices.append(vertex)
        return g

    @multidispatch(Edge)
    def __add__(self, edge: Edge) -> Self:
        g: Self = deepcopy(self)

        edge.predecessor.graph = g
        edge.successor.graph = g

        edge.predecessor += edge.successor
        edge.successor += edge.predecessor

        edge.graph = g

        g.edges.append(edge)
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
            repr_txt += f"w_{str(e.predecessor)}{str(e.successor)} = {e.value}"

        return repr_txt

    # This class is used only for tests
    class _DebugGraphviz():
        source: str = ""

    # dbg is passed as a object reference
    def _repr_svg_(self, dbg: _DebugGraphviz | None = None) -> ImportError | None:
        if not ipds:
            print("No IPython installed")
            return ImportError()

        if not gv:
            print("No GraphViz installed")
            return ImportError()

        g = gv.Digraph('G')

        for v in self.vertices:
            g.node(str(v))

        for e in self.edges:
            g.edge(str(e.predecessor), str(e.successor), label=str(e.value))

        if dbg:
            dbg.source = g.source

        ipds.display_svg(g)

        return None

    def _repr_png_(self, dbg: _DebugGraphviz | None = None) -> ImportError | None:
        if not ipds:
            print("No IPython installed")
            return ImportError()

        if not gv:
            print("No GraphViz installed")
            return ImportError()

        g = gv.Digraph('G')

        for v in self.vertices:
            g.node(str(v))

        for e in self.edges:
            g.edge(str(e.predecessor), str(e.successor), label=str(e.value))

        if dbg:
            dbg.source = g.source

        ipds.display_png(g)
        return None

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

