from __future__ import annotations

__all__ = ["Graph"]

from typing import TYPE_CHECKING, Self, Dict, Optional, Any
if TYPE_CHECKING: # pragma: no cover
    from .route import Route

from .vertex import Vertex
from .edge import Edge

from .algorithm import _Algorithm, _AlgorithmFunction, AlgorithmEnum
from .exception import LibgraphyError

import jsonpickle

from .utils import _ImgFormat, _DebugGraphviz

try:
    import graphviz as gv
except ImportError:
    gv = None

try:
    import IPython.display as ipds
except ImportError:
    ipds = None

from copy import deepcopy

class Graph:

    __algorithms: Dict[AlgorithmEnum, _AlgorithmFunction] = {
            AlgorithmEnum.DIJKSTRA: _Algorithm.dijkstra,
            AlgorithmEnum.BELLMANFORD: _Algorithm.bellmanFord
    }

    # TODO: implement incidence matrix
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

    # ********** Graph **********
    def _graph__iadd__(self, g: Graph) -> Graph:
        if self is g:
            raise LibgraphyError("Can't add the same graph")

        for v in self.vertices:
            v.graph = g
        for e in self.edges:
            e.graph = g

        g.vertices += self.vertices
        g.edges += self.edges

        return g

    def _graph__add__(self, g: Graph) -> Graph:
        vertices_len: int = len(self.vertices)
        edges_len: int = len(self.edges)

        g += self
        ng: Graph = deepcopy(g)

        # * Bringing self back *
        for _ in range(vertices_len):
            del g.vertices[-1]
        for _ in range(edges_len):
            del g.edges[-1]
        # **********************

        return ng
    # ***************************

    def __iadd__(self, element: Vertex | Edge | Graph) -> Graph:
        return element._graph__iadd__(self)

    def __add__(self, element: Vertex | Edge | Graph) -> Graph:
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

    def __rmul__(self, scalar: int | float) -> Graph:
        return self * scalar

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

    def _create_edge(self, precedessor: Vertex, successor: Vertex) -> Graph:
        self += Edge(precedessor, successor)
        return self

    def __draw_graph(self, format: ImgFormat, dbg: Optional[_DebugGraphviz] = None):
        if not ipds:
            raise ImportError("No IPython installed")

        if not gv:
            raise ImportError("No GraphViz installed")

        g = gv.Digraph('G')

        nodes: Dict[Vertex, int] = {}
        for i, v in enumerate(self.vertices):
            g.node(f"v{i}", label=str(v))
            nodes[v] = i

        for e in self.edges:
            p = nodes[e.predecessor]
            s = nodes[e.successor]
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

    def findPath(self, algorithm: AlgorithmEnum, start: Vertex, end: Vertex) -> Route:
        path_algorithm: _AlgorithmFunction = self.__algorithms[algorithm]
        r: Route = path_algorithm(self, start, end)
        return r

    def incidence(self, weighted: bool):
        # TODO
        pass

    def isGrid(self):
        # TODO
        pass

    @staticmethod
    def to_json(graph: Graph) -> str:
        # https://stackoverflow.com/a/42611918
        s = jsonpickle.encode(graph, indent=1)
        return s

    @staticmethod
    def write_to_json_file(graph: Graph, filename: str):
        json_str = Graph.to_json(graph)
        with open(filename, 'w+') as f:
            f.write(json_str)

    @staticmethod
    def from_json(json_str: str) -> Graph:
        g = jsonpickle.decode(json_str)
        return g

    @staticmethod
    def read_from_json_file(filename: str):
        json_str = ''
        with open(filename) as f:
            json_str = f.read()
        return Graph.from_json(json_str)

    @staticmethod
    def to_networkx(graph: Graph) -> None:
        # TODO
        pass

    @staticmethod
    def from_networkx(graph) -> None:
        # TODO
        pass

    @staticmethod
    def to_scigraph(graph: Graph) -> None:
        # TODO
        pass

    @staticmethod
    def from_scigraph(graph) -> None:
        # TODO
        pass

