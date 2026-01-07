from __future__ import annotations

__all__ = ["GraphFactory"]

import random
import sys
from random import *

from enum import Enum, auto

from .graph import Graph
from .vertex import Vertex
from .edge import Edge
from .exception import LibgraphyError

class GraphFactory:
    class TypeEnum(Enum):
        RANDOM = auto()
        GRAPH = auto()
        DIGRAPH = auto()
        GRID = auto()
        TRIANGLE_GRID = auto()
        SQUARE_GRID = auto()
        MAZE = auto()
        SQUARE_MAZE = auto()
        RING = auto()

    @staticmethod
    def graph(vertice_number:int, edge_number:int = -1, weighted:bool = False) -> Graph:
        # Sanity check
        if vertice_number <= 0:
            raise LibgraphyError(f"Cannot create a graph with {vertice_number} vertices")

        # Create graph and add vertices
        g = Graph()
        for i in range(vertice_number):
            g += Vertex(i)

        # Sanitize edge number
        max_edges = int(vertice_number * (vertice_number - 1) / 2)
        if edge_number < 0:
            edge_number = randint(1, max_edges)
        elif edge_number > max_edges:
            edge_number = max_edges

        # Add edges
        if edge_number < max_edges:
            current_edges = []

            while len(current_edges) < edge_number:
                i = randrange(1, vertice_number)
                j = randrange(0, i)
                if [i,j] not in current_edges:
                    current_edges.append([i,j])
                    if weighted:
                        weight = random()
                    else:
                        weight = 1
                    g += Edge(g.vertices[i], g.vertices[j], weight)
                    g += Edge(g.vertices[j], g.vertices[i], weight)

        else:
            for i in range(1,vertice_number):
                for j in range(0, i):
                    if weighted:
                        weight = random()
                    else:
                        weight = 1
                    g += Edge(g.vertices[i], g.vertices[j], weight)
                    g += Edge(g.vertices[j], g.vertices[i], weight)

        # return graph
        return g

    @staticmethod
    def complete_graph(vertice_number:int, weighted:bool = False) -> Graph:
        return GraphFactory.graph(vertice_number, sys.maxsize)

    @staticmethod
    def digraph(vertice_number:int, edge_number:int = -1, weighted:bool = False) -> Graph:
        # Sanity check
        if vertice_number <= 0:
            raise LibgraphyError(f"Cannot create a digraph with {vertice_number} vertices")

        # Create graph and add vertices
        g = Graph()
        for i in range(vertice_number):
            g += Vertex(i)

        # Sanitize edge number
        max_edges = vertice_number * (vertice_number - 1)
        if edge_number < 0:
            edge_number = randint(1, max_edges)
        elif edge_number > max_edges:
            edge_number = max_edges

        # Add edges
        if edge_number < max_edges:
            current_edges = []

            while len(current_edges) < edge_number:
                j = i = randrange(0, vertice_number)
                while j == i:
                    j = randrange(0, vertice_number)
                if [i, j] not in current_edges:
                    current_edges.append([i, j])
                    if weighted:
                        weight = random()
                    else:
                        weight = 1
                    g += Edge(g.vertices[i], g.vertices[j], weight)

        else:
            for i in range(0, vertice_number):
                for j in range(0, vertice_number):
                    if i==j:
                        continue
                    if weighted:
                        weight = random()
                    else:
                        weight = 1
                    g += Edge(g.vertices[i], g.vertices[j], weight)

        # return graph
        return g

    @staticmethod
    def complete_digraph(vertice_number:int, weighted:bool = False) -> Graph:
        return GraphFactory.digraph(vertice_number, sys.maxsize, weighted)

    @staticmethod
    def grid(vertice_number:int, degree:int) -> Graph:
        # Sanity check
        if vertice_number <= 0 or degree <= 0:
            raise LibgraphyError(f"Cannot create a {degree}-degree grid graph with {vertice_number} vertices")

        # Check if there are enough vertices to form a grid and the of the parity principle if fulfilled
        if (degree >= vertice_number) or (((degree * vertice_number)%2)!=0):
            raise LibgraphyError(f"Cannot create a {degree}-degree grid graph with {vertice_number} vertices")

        # Create graph and add vertices
        g = Graph()
        for i in range(vertice_number):
            g += Vertex(i)

        # Add edges
        offset = 1
        for i in range(vertice_number-1):
            v1 = g.vertices[i]
            offset -= 1
            while len(v1.neighbors) < degree:
                offset+=1
                if i+offset >= vertice_number:
                    offset = 1
                v2 = g.vertices[i+offset]
                if (v1.isConnected(v2)==False) and (len(v2.neighbors) < degree):
                    g += Edge(v1, v2, 1)
                    g += Edge(v2, v1, 1)

        # return graph
        return g

    @staticmethod
    def square_grid(width:int, height:int, edge_number:int = -1, diagonals:bool = True) -> Graph:
        # Sanity checks
        if width <= 1 or height <= 1:
            raise LibgraphyError(f"Cannot create square grid with ({width}, {height}) dimensions")

        # Normalize edge count
        max_edges = (width-1)*height + width*(height-1)
        if diagonals:
            max_edges += 2*(width-1)*(height-1)
        if edge_number > max_edges:
            edge_number = max_edges
        if edge_number < 0:
            edge_number = randrange(1, max_edges)

        # Create graph and vertices
        g = Graph()
        for y in range(height):
            for x in range(width):
                g += Vertex(f"({x},{y})", x=x, y=y)

        # Exclude random edges
        directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        if diagonals:
            directions.extend([[-1, -1], [-1, 1], [1, -1], [1, 1]])
        excluded_edges = []
        while len(excluded_edges) < max_edges - edge_number:
            direction = directions[randrange(0, len(directions))]
            v1 = g.vertices[randrange(0, len(g.vertices)-1)]
            x2 = v1.x+direction[0]
            y2 = v1.y+direction[1]
            if x2 >= width or x2 < 0 or y2 >= height or y2 < 0:
                continue
            v2 = g.vertices[y2*width+x2]
            if [v1,v2] not in excluded_edges and [v2,v1] not in excluded_edges:
                excluded_edges.append([v1, v2])

        # Add edges
        for y in range(height):
            for x in range(width):
                v1 = g.vertices[y*width+x]
                neighbors = []
                for direction in directions:
                    x2 = x+direction[0]
                    y2 = y+direction[1]
                    if x2 >= width or x2 < 0 or y2 >= height or y2 < 0:
                        continue
                    neighbors.append(g.vertices[y2*width+x2])
                for v2 in neighbors:
                    if [v1, v2] not in excluded_edges and [v2, v1] not in excluded_edges:
                        if v2 not in v1.neighbors:
                            g += Edge(v1, v2, 1)
                        if v1 not in v2.neighbors:
                            g += Edge(v2, v1, 1)

        # return graph
        return g

    @staticmethod
    def triangle_grid(width:int, height:int, edge_number:int = -1) -> Graph:
        # Sanity checks
        if width <= 1 or height <= 1:
            raise LibgraphyError(f"Cannot create triangle grid with [{width}, {height}] dimensions")

        # Normalize edge count
        max_edges = 3*width*height - 2*width - 2*height + 1
        if edge_number > max_edges:
            edge_number = max_edges
        if edge_number < 0:
            edge_number = randrange(1, max_edges)

        # Create graph and vertices
        g = Graph()
        for y in range(height):
            for x in range(width):
                offset = 0
                if y%2 == 1:
                    offset += 0.5
                g += Vertex(f"({x+offset},{y})", x=x+offset, y=y)

        # Exclude random edges
        excluded_edges = list(range(max_edges))
        shuffle(excluded_edges)
        excluded_edges = excluded_edges[:max_edges-edge_number]

        # Add edges
        edge = -1
        for i in range(len(g.vertices)):
            v1 = g.vertices[i]
            if i-width+1 >= 0:
                v2 = g.vertices[i-width+1]
                if v1.y != v2.y:
                    if edge+1 not in excluded_edges:
                        g += Edge(v1, v2, 1)
                        g += Edge(v2, v1, 1)
                    edge+=1
            if (i+1)%width != 0:
                if edge+1 not in excluded_edges:
                    v2 = g.vertices[i+1]
                    g += Edge(v1, v2, 1)
                    g += Edge(v2, v1, 1)
                edge+=1
            if i+width < len(g.vertices):
                if edge+1 not in excluded_edges:
                    v2 = g.vertices[i+width]
                    g += Edge(v1, v2, 1)
                    g += Edge(v2, v1, 1)
                edge+=1

        # return graph
        return g

    @staticmethod
    def maze(vertice_number:int, start_vertex:int = -1, end_vertex:int = -1) -> Graph:
        # Sanity checks
        if vertice_number < 1:
            raise LibgraphyError(f"Cannot create maze with {vertice_number} vertices")
        if start_vertex == end_vertex and start_vertex>=0:
            raise LibgraphyError(f"Cannot create maze with same starting and ending point")
        if start_vertex >= vertice_number or end_vertex >= vertice_number:
            raise LibgraphyError(f"Maze start or end out of bounds")

        # Set start and end vertices
        if start_vertex == -1:
            start_vertex = end_vertex
        while start_vertex == end_vertex:
            start_vertex = randrange(0, vertice_number)
        if end_vertex == -1:
            end_vertex = start_vertex
            while end_vertex == start_vertex:
                end_vertex = randrange(0, vertice_number)

        # Create graph and vertices
        g = Graph()
        for i in range(vertice_number):
            g += Vertex(i)

        # Randomize vertices order
        free_vertices = list(range(vertice_number))
        shuffle(free_vertices)
        free_vertices.insert(0, free_vertices.pop(free_vertices.index(end_vertex)))
        free_vertices.remove(start_vertex)
        Q = [start_vertex]

        # Build maze
        while len(Q) and len(free_vertices):
            v1_id = Q.pop(randrange(0, len(Q)))
            degree = randint(1, min(3, len(free_vertices)))
            for i in range(degree):
                v2_id = free_vertices.pop()
                Q.append(v2_id)

                v1 = g.vertices[v1_id]
                v2 = g.vertices[v2_id]

                g += Edge(v1, v2)
                g += Edge(v2, v1)

        # return graph
        return g

    @staticmethod
    def square_grid_maze(width:int, height:int) -> Graph:
        # Sanity checks
        if width < 1 or height < 1:
            raise LibgraphyError(f"Cannot create maze with [{width},{height}] dimensions")

        # Create graph and vertices
        g = Graph()
        free_vertices = []
        for y in range(height):
            for x in range(width):
                g += Vertex(f"({x},{y})", x=x, y=y)
                free_vertices.append((x,y))

        # Randomize vertices order
        connected = [free_vertices.pop(0)]
        ignored = []

        # Build maze
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        while len(free_vertices):
            v1_pos = connected[randrange(0, len(connected))]
            if v1_pos in ignored:
                continue

            v2_pos = None
            directionsCopy = directions.copy()
            while v2_pos == None:
                if len(directionsCopy) == 0:
                    connected.remove(v1_pos)
                    ignored.append(v1_pos)
                    break

                direction = directionsCopy[randrange(0, len(directionsCopy))]
                v2_pos = (v1_pos[0] + direction[0], v1_pos[1] + direction[1])
                if (v2_pos not in connected and v2_pos not in ignored
                        and v2_pos[0] >= 0 and v2_pos[1] >= 0 and v2_pos[0] < width and v2_pos[1] < height):
                    v1 = g.vertices[v1_pos[1] * width + v1_pos[0]]
                    v2 = g.vertices[v2_pos[1] * width + v2_pos[0]]

                    g += Edge(v1, v2, 1)
                    g += Edge(v2, v1, 1)

                    connected.append(v2_pos)
                    free_vertices.remove(v2_pos)
                else:
                    v2_pos = None
                    directionsCopy.remove(direction)

        return g

    @staticmethod
    def ring(vertice_number:int, directed:bool = False) -> Graph:
        # Sanity checks
        if vertice_number < 1:
            raise LibgraphyError(f"Cannot create ring with {vertice_number} vertices")

        # Create graph
        g = Graph()

        last_vertex = None
        for i in range(vertice_number):
            v = Vertex(i)
            g += v
            if last_vertex != None:
                g += Edge(last_vertex, v)
                if not directed:
                    g += Edge(v, last_vertex)
            last_vertex = v

        # Loop
        g += Edge(last_vertex, g.vertices[0])
        if not directed:
            g += Edge(g.vertices[0], last_vertex)

        # return graph
        return g

    @staticmethod
    def generic(type:TypeEnum = TypeEnum.RANDOM, params:dict = {}) -> Graph:
        # Bind params
        if params is None:
            params = {}
        if isinstance(params, dict):
            vertice_number = params.get("vertice_number", randint(3,30))
            edge_number = params.get("edge_number", -1)
            weighted = params.get("weighted", False)
            degree = params.get("degree", 3)
            diagonals = params.get("diagonals", True)
            width = params.get("width", randint(5, 10))
            height = params.get("height", randint(5, 10))
            start_vertex = params.get("start_vertex", -1)
            end_vertex = params.get("end_vertex", -1)
            directed = params.get("directed", False)
        else:
            raise LibgraphyError(f"Argument 2 of \"GraphFactory.graph\" needs to be a dictionary.")

        # Generate graph of given type
        while type == GraphFactory.TypeEnum.RANDOM:
            type = choice(list(GraphFactory.TypeEnum))
        if type == GraphFactory.TypeEnum.GRAPH:
            return GraphFactory.graph(vertice_number, weighted)
        elif type == GraphFactory.TypeEnum.DIGRAPH:
            return GraphFactory.digraph(vertice_number, edge_number, weighted)
        elif type == GraphFactory.TypeEnum.GRID:
            return GraphFactory.grid(vertice_number, degree)
        elif type == GraphFactory.TypeEnum.SQUARE_GRID:
            return GraphFactory.square_grid(width, height, edge_number, diagonals)
        elif type == GraphFactory.TypeEnum.TRIANGLE_GRID:
            return GraphFactory.triangle_grid(width, height, edge_number)
        elif type == GraphFactory.TypeEnum.MAZE:
            return GraphFactory.maze(vertice_number, start_vertex, end_vertex)
        elif type == GraphFactory.TypeEnum.SQUARE_MAZE:
            return GraphFactory.square_grid_maze(width, height)
        elif type == GraphFactory.TypeEnum.RING:
            return GraphFactory.ring(vertice_number, directed)
        else:
            raise LibgraphyError(f"Unknown graph type: {type}")