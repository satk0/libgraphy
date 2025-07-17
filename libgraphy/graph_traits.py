from .graph import Graph
from .vertex import Vertex
from .exception import LibgraphyError

class GraphTraits:

    def __init__(self) -> None:
        self.is_weighted: bool = False
        self.is_directional: bool = False
        self.is_grid: bool = False
        self.grid_level: int = 0
        self.has_cycles: bool = False
        self.is_full: bool = False
        self.is_empty: bool = False

    def check_if_weighted(self, g: Graph) -> None:
        for e in g:
            if e.value != 1:
                self.is_weighted = True
                return
        self.is_weighted = False

    def check_if_directional(self, g: Graph) -> None:
        visited: set[Vertex] = set()

        for v in g:
            for n in v:
                if n in visited:
                    continue
                if v not in n.neighbors:
                    self.is_directional = True
                    return
            visited.add(v)

        self.is_directional = False

    def check_if_grid(self, g: Graph) -> None:
        self.is_grid = self.check_if_weighted(g) is False and \
                self.check_if_directional(g) is False

    def get_grid_level(self, g: Graph) -> None:
        if self.is_grid is False:
            raise LibgraphyError("Graph is not a grid!")
        for v in g:
            self.grid_level = max(self.grid_level, len(v.neighbors))

    def check_if_has_cycles(self, g: Graph) -> None:
        # TODO: implement
        pass

    def check_if_full(self, g: Graph) -> None:
        n = len(g.vertices)
        self.is_full = (len(g.edges) == n*(n-1)/2)

    def check_if_empty(self, g: Graph) -> None:
        if g.edges is []:
           self.is_empty = True
        self.is_empty = False

