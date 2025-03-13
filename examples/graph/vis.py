from libgraphy import *
from IPython.display import (
    display_svg, display_latex
)

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

display_svg(g)
display_latex(g)
