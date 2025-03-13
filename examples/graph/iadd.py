from libgraphy import Graph, Vertex, Edge

v1, v2 = Vertex('1'), Vertex('2')
e1 = Edge(v1, v2)
g1 = Graph()
g1 += v1
g1 += v2
g1 += e1

v3, v4 = Vertex('3'), Vertex('4')
e2 = Edge(v3, v4)
g2 = Graph()
g2 += v3
g2 += v4
g2 += e2

g1 += g2
print(g1) # {1, 2, 3, 4}; 1 -> 2, 3 -> 4
