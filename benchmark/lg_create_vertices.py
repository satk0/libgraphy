from libgraphy import *
import sys

n = int(sys.argv[1])

g = Graph()
for i in range(n):
    g += Vertex(i)
