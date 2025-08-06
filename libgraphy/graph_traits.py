from .graph import Graph
from .vertex import Vertex
from .exception import LibgraphyError

# TODO: Test
class GraphTraits:

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
    def get_traits(g: Graph) -> "GraphTraits":
        gt: GraphTraits = GraphTraits(g)
        gt.check_if_grid()
        gt.get_grid_level()
        gt.check_if_negative()
        gt.check_if_has_cycles()
        gt.check_if_full()
        gt.check_if_empty()

        return gt

