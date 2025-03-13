from libgraphy import Vertex, Graph

g = Graph()
v = Vertex()
g += v # OK
g += v # ERROR
