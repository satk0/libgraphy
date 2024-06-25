from typing import Dict


class Vertex:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.neighbors: list[int] =  []


class Edge:
    def __init__(self, source: int, destination: int, weight: int) -> None:
        self.source: int = source
        self.destination: int = destination
        self.weight = weight


class Graph:
    def __init__(self) -> None:
        self.vertices: Dict[int, Vertex] = {}
        self.edges: list[Edge] = []

    def add_vertex(self, id: int) -> None:
        self.vertices[id] = Vertex(id)

    def add_edge(self, source: int, destination: int, weight: int) -> None:
        self.edges.append(Edge(source, destination, weight))

        self.vertices[source].neighbors.append(destination)
        self.vertices[destination].neighbors.append(source)

    def print(self):
        print("Vertices:")

        vertex_txt = '{'
        for v in self.vertices.keys():
            vertex_txt += f'{v}, '

        vertex_txt = vertex_txt.removesuffix(', ')
        vertex_txt += '}'
        print(vertex_txt)

        print("Edges:")
        for e in self.edges:
            print(f"w_{e.source}{e.destination} = {e.weight}")


g = Graph()

g.add_vertex(1)
g.add_vertex(2)

g.add_edge(1, 2, 10)

g.print()

