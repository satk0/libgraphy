import random

import networkx as nx

def in_edges(v1, v2, edges) -> bool:
    for e in edges:
        if v1 is e[0] and v2 is e[1]:
            return True
    return False

def generate_edges(no_edges: int) -> list:
    edges = []
    for _ in range(no_edges):
        appended = False

        while not appended:
            v1 = random.choice(vertices)
            v2 = random.choice(vertices)
            value = random.randint(1, 100) # positive

            if v1 != v2 and not in_edges(v1, v2, edges):
                edges.append([v1, v2, value])
                appended = True
    return edges

def max_hops_dijkstra(n: int, edges: list) -> list:
    G = nx.DiGraph()
    for e in edges:
        G.add_edge(e[0], e[1], weight=e[2])

    max_s, max_t, max_hops = 0, 0, 0
    for s in range(n):
        for t in range(n):
            if s == t:
                continue
            try:
                path = nx.dijkstra_path(G, s, t)
            except:
                continue
            hops = len(path)
            if hops > max_hops:
                max_s, max_t, max_hops = s, t, hops

    return [max_s, max_t, max_hops]


list_of_edges = []
for n in range(10, 20 * 10 + 1, 10):
    vertices = [v for v in range(n)]

    print("1. Generating edges...")
    print(f"n = {n}")

    max_edges = n * (n-1) + 1 # digraph so x2

    no_edges = random.randrange(max_edges // 3, max_edges)
    print(no_edges)

    edges = generate_edges(no_edges)
    s, t, hops = max_hops_dijkstra(n, edges)

    print("MAX_HOPS -", hops)
    print(f"s = {s} | t = {t}")
    print("number of edges:", len(edges))
    list_of_edges.append([edges, [s, t], hops])

fname = "generated/dijkstra_edges.txt"
print(f"2. Writing edges to '{fname}' file...")

with open(fname, 'w+') as f:
    for edges in list_of_edges:
        f.write(f"{edges}\n")

print("Done.")
