import sys
import json
from libgraphy import *

edges = json.loads(sys.argv[1])

n = 50

g = Graph()

for i in range(n):
    g += Vertex(i)

for e in edges:
    g += Edge(g.vertices[e[0]], g.vertices[e[1]], e[2])
