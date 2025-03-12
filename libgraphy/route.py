from __future__ import annotations

__all__ = ["Route"]

from typing import TYPE_CHECKING, Self, Dict
if TYPE_CHECKING: # pragma: no cover
    from .graph import Graph
    from .vertex import Vertex

from .utils import _ImgFormat, _DebugGraphviz

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


    def __draw_graph(self, format: _ImgFormat, dbg: Optional[_DebugGraphviz] = None):
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

        if format == _ImgFormat.PNG:
            ipds.display_png(g)
        elif format == _ImgFormat.SVG:
            ipds.display_svg(g)

    # dbg is passed as a object reference
    def _repr_svg_(self, dbg: _DebugGraphviz | None = None):
        self.__draw_graph(_ImgFormat.SVG, dbg)

    def _repr_png_(self, dbg: _DebugGraphviz | None = None):
        self.__draw_graph(_ImgFormat.PNG, dbg)

    # get i-th edge
    def __getitem__(self, key: int) -> Edge:
        return self.edges[key]

    def __imul__(self, scalar: int | float) -> Self:
        self.edges = [Edge(e.predecessor, e.successor, e.value * scalar, e.graph) for e in self.edges]
        self.value *= scalar
        return self

    def __mul__(self, scalar: int | float) -> Route:
        prev_edges = self.edges
        prev_value = self.value

        self *= scalar
        r = deepcopy(self)

        self.edges = prev_edges
        self.value = prev_value

        return r

    def __rmul__(self, scalar: int | float) -> Route:
        return self * scalar

