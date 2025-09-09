from libgraphy import *
from IPython.display import (
    display_png
)

vertices = [Vertex(l) for l in "stxyz"]
s, t, x, y, z = vertices

edges = [Edge(s, t, 10), Edge(t, y, 2), Edge(y, x, 9),
         Edge(z, s, 7), Edge(y, z, 2), Edge(s, y, 5),
         Edge(y, t, 3), Edge(t, x)]

g = Graph()
for v in vertices:
    g += v

for e in edges:
    g += e

path: Path = g.find_path(s, x, algorithm = AlgorithmEnum.DIJKSTRA)

display_png(path)
