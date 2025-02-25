import json
from time import time

import networkx as nx


def nx_create_graph(n: int, edges: list) -> nx.DiGraph:
    g = nx.DiGraph()

    for i in range(n):
        g.add_node(i)

    for e in edges:
        g.add_edge(e[0], e[1], weight=e[2])

    return g


data = []
with open("generated/dijkstra_edges.txt") as f:
    n = 10
    for l in f:
        edges, vertices, hops = json.loads(l)
        s, t = vertices
        print("vertices:", n)

        nx_g = nx_create_graph(n, edges)

        total, _ = nx.single_source_dijkstra(nx_g, s, t)

        print(len(edges), total)
        data.append([len(edges), hops, total])

        n += 10

print("Saving to file...")
with open(f"res/dijkstra/dijkstra_data.txt", 'w+') as f:
    for t in data:
        f.write(f'{t}\n')

print("Done.")
