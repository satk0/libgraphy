from __future__ import annotations

__all__ = ["Route"]

from typing import TYPE_CHECKING, Self, Dict
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph
    from .vertex import Vertex

from enum import Enum

try:
    import graphviz as gv
except ImportError:
    gv = None

try:
    import IPython.display as ipds
except ImportError:
    ipds = None

from .edge import Edge

from copy import deepcopy

class Route:
    def __init__(self, graph: Graph) -> None:
        self.graph: Graph = graph

        self.edges: list[Edge] = []
        self.value: int | float = 0

    def __repr__(self) -> str:
        repr_txt = f"Route: {self.edges[0].predecessor}"
        s = 0
        for e in self.edges:
            repr_txt += f' -> {str(e.successor)}'
            s += e.value

        repr_txt += '\n'
        repr_txt += f'Value: {s}'

        return repr_txt

    def __in_edges(self, vertex: Vertex) -> bool:
        for e in self.edges:
            if vertex in [e.predecessor, e.successor]:
                return True
        return False

    # TODO: Put it somewhere
    class _DebugGraphviz():
        source: str = ""

    class __GraphImgFormat(Enum): 
        PNG = 1
        SVG = 2

    def __draw_graph(self, format: __GraphImgFormat, dbg: Optional[_DebugGraphviz] = None):
        if not ipds:
            raise ImportError("No IPython installed")

        if not gv:
            raise ImportError("No GraphViz installed")

        g = gv.Digraph('G')

        nodes: Dict[Vertex, int] = {}
        for i, v in enumerate(self.graph.vertices):
            if self.__in_edges(v):
                g.node(f"v{i}", label=str(v), color='green', fontcolor='darkgreen')
            else:
                g.node(f"v{i}", label=str(v))
            nodes[v] = i

        for e in self.graph.edges:
            p = nodes[e.predecessor]
            s = nodes[e.successor]
            if e in self.edges:
                g.edge(f"v{p}", f"v{s}", label=str(e.value), color='green', fontcolor='darkgreen')
            else:
                g.edge(f"v{p}", f"v{s}", label=str(e.value))

        if dbg:
            dbg.source = g.source

        if format == self.__GraphImgFormat.PNG:
            ipds.display_png(g)
        elif format == self.__GraphImgFormat.SVG:
            ipds.display_svg(g)

    # dbg is passed as a object reference
    def _repr_svg_(self, dbg: _DebugGraphviz | None = None):
        self.__draw_graph(self.__GraphImgFormat.SVG, dbg)

    def _repr_png_(self, dbg: _DebugGraphviz | None = None):
        self.__draw_graph(self.__GraphImgFormat.PNG, dbg)

    # get i-th edge
    def __getitem__(self, key: int) -> Edge:
        return self.edges[key]

    def __imul__(self, scalar: int | float) -> Self:
        self.edges = [Edge(e.predecessor, e.successor, e.value * scalar, e.graph) for e in self.edges]
        return self

    def __mul__(self, scalar: int | float) -> Route:
        tmp_edges = self.edges

        self *= scalar
        r = deepcopy(self)

        self.edges = tmp_edges

        return r

    def __rmul__(self, scalar: int | float) -> Route:
        return self * scalar

