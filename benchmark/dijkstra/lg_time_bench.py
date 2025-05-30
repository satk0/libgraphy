from libgraphy import *
import csv
from time import time

vertices = [Vertex(l) for l in "stxyz"]
s, t, x, y, z = vertices

edges = [Edge(s, t, 10), Edge(t, y, 2), Edge(y, x, 9),
     Edge(x, z, 4), Edge(z, x, 6), Edge(z, s, 7),
     Edge(y, z, 2), Edge(s, y, 5), Edge(y, t, 3), Edge(t, x)]

g = Graph()
for v in vertices:
    g += v

for e in edges:
    g += e

with open('lg_time.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    for n in range(100000, 1000001, 100000):
        start = time()
        for _ in range(n):
            g.findPath(AlgorithmEnum.DIJKSTRA, s, x)
        end = time()

        tm = end - start
        print(n, tm)
        csvwriter.writerow([n, tm])





