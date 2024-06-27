from typing import Dict
try:
    import graphviz as gv
except ImportError:
    gv = None

try:
    import IPython.display as ipds
except ImportError:
    ipds = None


class Vertex:
    def __init__(self, id: int, weight: int = 0) -> None:
        self.id: int = id
        self.neighbors: list[int] =  []
        self.weight: int = weight


class Edge:
    def __init__(self, source: int, destination: int, weight: int = 0) -> None:
        self.source: int = source
        self.destination: int = destination
        self.weight: int = weight


class Graph:
    def __init__(self) -> None:
        self.vertices: Dict[int, Vertex] = {}
        self.edges: list[Edge] = []

    def __repr__(self):
        repr_txt = "Vertices:\n"

        repr_txt += '{'
        for v in self.vertices.keys():
            repr_txt += f'{v}, '

        repr_txt = repr_txt.removesuffix(', ')
        repr_txt += '}\n'

        repr_txt += "Edges:\n"
        for e in self.edges:
            repr_txt += f"w_{e.source}{e.destination} = {e.weight}"

        return repr_txt


    def add_vertex(self, id: int) -> None:
        self.vertices[id] = Vertex(id)

    def add_edge(self, source: int, destination: int, weight: int) -> None:
        self.edges.append(Edge(source, destination, weight))

        self.vertices[source].neighbors.append(destination)
        self.vertices[destination].neighbors.append(source)


    def _repr_svg_(self):
        if not ipds:
            print("No IPython imported")
            return

        if not gv:
            print("No GraphViz installed")
            return

        g = gv.Digraph('G')

        for _, v in self.vertices.items():
            g.node(str(v.id))

        for e in self.edges:
            g.edge(str(e.source), str(e.destination), label=str(e.weight))

        ipds.display_svg(g)

    def _repr_png_(self):
        if not ipds:
            print("No IPython imported")
            return

        if not gv:
            print("No GraphViz installed")
            return

        g = gv.Digraph('G')

        for _, v in self.vertices.items():
            g.node(str(v.id))

        for e in self.edges:
            g.edge(str(e.source), str(e.destination), label=str(e.weight))

        ipds.display_png(g)

    def _repr_latex_(self):
        latex_txt = r"$$\begin{gathered}" + '\n'

        latex_txt += "Vertices:"
        latex_txt += " \\\\ \n"

        latex_txt += "\{"
        for v in self.vertices.keys():
            latex_txt += f'{v},'
        latex_txt = latex_txt.removesuffix(',')
        latex_txt += "\} \\\\ \n"

        latex_txt += "Edges:"
        latex_txt += " \\\\ \n"

        for e in self.edges:
            latex_txt += r"w_{%d%d} = %d \\" % (e.source, e.destination, e.weight) + '\n'

        latex_txt += r"\end{gathered}$$"

        return latex_txt

