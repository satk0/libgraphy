import networkx as nx
import csv

from time import time


G = nx.DiGraph()

vertices = [l for l in "stxyz"]
s, t, x, y, z = vertices
edges = [(s, t, 10), (t, y, 2), (y, x, 9),
    (x, z, 4), (z, x, 6), (z, s, 7),
    (y, z, 2), (s, y, 5), (y, t, 3), (t, x, 1)]

for e in edges:
    G.add_edge(e[0], e[1], weight=e[2])

with open('nx_time.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    for n in range(100000, 1000001, 100000):
        start = time()
        for _ in range(n):
            nx.dijkstra_path(G, s, x)
        end = time()

        tm = end - start
        print(n, tm)
        csvwriter.writerow([n, tm])

