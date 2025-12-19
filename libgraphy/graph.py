from __future__ import annotations

__all__ = ["Graph"]

from typing import TYPE_CHECKING, Self, Dict, Optional, Any, cast, Literal
if TYPE_CHECKING: # pragma: no cover
    from .path import Path

from .heuristic import Heuristic

from .vertex import Vertex
from .edge import Edge, _EdgeList

from .algorithm import _Algorithm, _AlgorithmFunction, AlgorithmEnum
from .exception import LibgraphyError

import jsonpickle

from .utils import _ImgFormat, _DebugGraphviz

try:
    import graphviz as gv
    gv_found = True
except ImportError:
    gv_found = False

try:
    import networkx as nx
    nx_found = True
except ImportError:
    nx_found = False

try:
    from scipy.sparse import csr_matrix
    scipy_found = True
except ImportError:
    scipy_found = False

try:
    import IPython.display as ipds
    ipds_found = True
except ImportError:
    ipds_found = False

from copy import deepcopy

class Graph:

    class Traits:

        def __init__(self, g: Graph) -> None:
            self.graph: Graph = g
            self.is_weighted: bool|None = None
            self.is_negative: bool|None = None
            self.is_directional: bool|None = None
            self.is_grid: bool|None = None
            self.grid_level: int|None = None
            self.has_cycles: bool|None = None
            self.is_full: bool|None = None
            self.is_empty: bool|None = None

        def check_if_weighted(self) -> None:
            for e in self.graph.edges:
                if e.value != 1:
                    self.is_weighted = True
                    return
            self.is_weighted = False

        # TODO: test
        def check_if_negative(self) -> None:
            for e in self.graph.edges:
                if e.value < 0:
                    self.is_negative = True
                    return
            self.is_negative = False

        def check_if_directional(self) -> None:
            visited: set[Vertex] = set()

            for v in self.graph.vertices:
                for e in v.adjacent_edges:
                    s = e.successor
                    if s in visited:
                        continue

                    directed_check = True
                    for se in s.adjacent_edges:
                        if se.successor is v and se.value == e.value:
                            directed_check = False

                    if directed_check:
                        self.is_directional = True
                        return

                visited.add(v)

            self.is_directional = False

        def check_if_grid(self) -> None:
            self.check_if_weighted()
            self.check_if_directional()
            self.is_grid = (self.is_weighted is False and \
                    self.is_directional is False)

        def get_grid_level(self) -> None:
            if self.is_grid is None:
                raise LibgraphyError("Check first if graph is a grid!")
            if self.is_grid is False:
                return
            self.grid_level = 0
            for v in self.graph.vertices:
                self.grid_level = max(self.grid_level, len(v.neighbors))

        def _cycles_util(self, v: Vertex, visited: dict[Vertex, bool], rec_stack: dict[Vertex, bool]):

          if rec_stack[v]:
            return True # Vertex already in a stack -> Cycle detected

          if visited[v]:
            return False

          visited[v] = True
          rec_stack[v] = True

          for n in v:
            if self._cycles_util(n, visited, rec_stack):
                return True

          rec_stack[v] = False
          return False

        def check_if_has_cycles(self) -> None:
            # Based on:
            # https://www.geeksforgeeks.org/dsa/detect-cycle-in-a-graph/
            visited: dict[Vertex, bool] = {} # Track visited vertices
            rec_stack: dict[Vertex, bool] = {} # Track visited vertices

            for v in self.graph.vertices:
              visited[v] = False
              rec_stack[v] = False

            for v in self.graph.vertices:
              if not visited[v] and self._cycles_util(v, visited, rec_stack):
                self.has_cycles = True # Cycle found
                return

            self.has_cycles = False # No cycle found
            return

        def check_if_full(self) -> None:
            n = len(self.graph.vertices)
            self.is_full = (len(self.graph.edges) == n*(n-1))

        def check_if_empty(self) -> None:
            if self.graph.edges == []:
               self.is_empty = True
               return
            self.is_empty = False

        @staticmethod
        def get_traits(g: Graph) -> Graph.Traits:
            gt: Graph.Traits = Graph.Traits(g)
            gt.check_if_grid()
            gt.get_grid_level()
            gt.check_if_negative()
            gt.check_if_has_cycles()
            gt.check_if_full()
            gt.check_if_empty()

            return gt


    __algorithms: Dict[AlgorithmEnum, _AlgorithmFunction] = {
            AlgorithmEnum.DIJKSTRA: _Algorithm.dijkstra,
            AlgorithmEnum.BELLMAN_FORD: _Algorithm.bellman_ford,
            AlgorithmEnum.BEST: _Algorithm.best,
            AlgorithmEnum.A_STAR: _Algorithm.a_star
    }

    # TODO: implement incidence matrix
    def __init__(self, incidence_matrix = None) -> None:
        self.vertices: list[Vertex] = []
        self.edges: _EdgeList[Edge] = _EdgeList()

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

    def __draw_graph(self, format: _ImgFormat, dbg: Optional[_DebugGraphviz] = None):
        if not ipds_found:
            raise ImportError("No IPython installed")

        if not gv_found:
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

    def find_path(self, start: Vertex, end: Vertex, heuristic: Heuristic = Heuristic(), algorithm: AlgorithmEnum = AlgorithmEnum.BEST) -> Path:
        path_algorithm: _AlgorithmFunction = self.__algorithms[algorithm]
        p: Path = path_algorithm(self, start, end, heuristic)
        return p

    def incidence(self, weighted: bool):
        # TODO
        pass

    @staticmethod
    def to_json(graph: Graph) -> str:
        # https://stackoverflow.com/a/42611918
        s = str(jsonpickle.encode(graph, indent=1))
        return s

    @staticmethod
    def write_to_json_file(graph: Graph, filename: str) -> None:
        json_str = Graph.to_json(graph)
        with open(filename, 'w+') as f:
            f.write(json_str)

    @staticmethod
    def from_json(json_str: str) -> Graph:
        g: Graph = cast(Graph, jsonpickle.decode(json_str))
        return g

    @staticmethod
    def read_from_json_file(filename: str):
        json_str = ''
        with open(filename) as f:
            json_str = f.read()
        return Graph.from_json(json_str)

    # TODO: Test
    @staticmethod
    def to_networkx(graph: Graph) -> nx.DiGraph:
        if not nx_found:
            raise ImportError("No NetworkX installed")

        G = nx.DiGraph()

        names: dict[str, int] = dict()
        vertices: dict[Vertex, Any] = dict()

        for v in graph.vertices:
            if v.name in names.keys():
                name = "{}_{}".format(v.name, names[v.name])
                names[v.name] += 1
            else:
                names[v.name] = 0
                name = v.name

            G.add_node(name)
            vertices[v] = name

        for e in graph.edges:
            p = vertices[e.predecessor]
            s = vertices[e.successor]
            G.add_edge(p, s, weight=e.value)

        return G

    # TODO: Test
    @staticmethod
    def from_networkx(graph: nx.DiGraph) -> Graph:
        if not nx_found:
            raise ImportError("No NetworkX found!")

        g: Graph = Graph()
        vertices: dict[Any, Vertex] = {}

        for node in graph:
            v = Vertex(node)
            g += v

            vertices[node] = v

        for edge in graph.edges(data=True):
            p = vertices[edge[0]]
            s = vertices[edge[1]]
            g += Edge(p, s, edge[2]["weight"])

        return g

    @staticmethod
    def to_csgraph(graph: Graph) -> csr_matrix:
        if not scipy_found:
            raise ImportError("No SciPy found!")

        n: int = len(graph.vertices)
        adjacency_matrix: list[list[int]] = [ [0]*n for _ in range(n) ]
        names: Dict[Vertex, int] = {
            vertex: i for i, vertex in enumerate(graph.vertices)
        }

        for e in graph.edges:
            p = names[e.predecessor]
            s = names[e.successor]

            v = e.value
            if not isinstance(v, (int, float)):
                raise LibgraphyError("Edge value not float or integer")

            adjacency_matrix[p][s] = e.value

        return csr_matrix(adjacency_matrix)

    @staticmethod
    def from_csgraph(graph: csr_matrix) -> Graph:
        if not scipy_found:
            raise ImportError("No SciPy found!")

        cx = graph.tocoo()

        g: Graph = Graph()
        for i in range(cx.shape[0]):
            g += Vertex(i)

        for i,j,v in zip(cx.row, cx.col, cx.data):
            g += Edge(g.vertices[i], g.vertices[j], v)

        return g

    def get_traits(self) -> Graph.Traits:
        gt: Graph.Traits = Graph.Traits(self)
        gt.check_if_grid()
        gt.get_grid_level()
        gt.check_if_negative()
        gt.check_if_has_cycles()
        gt.check_if_full()
        gt.check_if_empty()

        return gt

