import json
from time import time

import numpy as np
from libgraphy import *
import networkx as nx
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import csgraph_from_dense
from scipy.sparse.csgraph import dijkstra

RUNS=10

def lg_create_graph(n: int, edges: list) -> Graph:
    g = Graph()

    for i in range(n):
        g += Vertex(i)

    for e in edges:
        g += Edge(g.vertices[e[0]], g.vertices[e[1]], e[2])

    return g

def nx_create_graph(n: int, edges: list) -> nx.DiGraph:
    g = nx.DiGraph()

    for i in range(n):
        g.add_node(i)

    for e in edges:
        g.add_edge(e[0], e[1], weight=e[2])

    return g

def scg_create_graph(n: int, edges: list):
    sparse_matrix = csr_matrix((n,n), dtype=np.int8).toarray()
    for e in edges:
        sparse_matrix[e[0], e[1]] = e[2]

    g = csgraph_from_dense(sparse_matrix)
    return g

def lg_bench(g: Graph, s, t) -> float:
    s, t = g.vertices[s], g.vertices[t]

    start = time()
    g.find_path(s, t, algorithm = AlgorithmEnum.DIJKSTRA)
    end = time()

    return end - start

def nx_bench(g: nx.DiGraph, s, t) -> float:
    start = time()
    nx.dijkstra_path(g, s, t)
    end = time()

    return end - start

def scg_bench(g, s) -> float:
    start = time()
    dijkstra(g, indices=s, directed=True)
    end = time()

    return end - start

for i in range(RUNS):
    print(f"*** ITERATION {i} ***")
    times = []
    with open("generated/dijkstra_edges.txt") as f:
        n = 10
        for l in f:
            edges, vertices, hops = json.loads(l)
            s, t = vertices
            print("vertices:", n)

            lg_g = lg_create_graph(n, edges)
            nx_g = nx_create_graph(n, edges)
            scg_g = scg_create_graph(n, edges)

            lg_tm = lg_bench(lg_g, s, t)
            nx_tm = nx_bench(nx_g, s, t)
            scg_tm = scg_bench(scg_g, s)

            print(len(edges), lg_tm, nx_tm, scg_tm)
            times.append([len(edges), hops, lg_tm, nx_tm, scg_tm])

            n += 10

    print("Saving to file...")
    with open(f"res/dijkstra/dijkstra_times_{i}.txt", 'w+') as f:
        for t in times:
            f.write(f'{t}\n')

print("Done.")
