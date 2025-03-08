from libgraphy import Graph, Edge

g = Graph()
e = Edge("1", "2")

g += e
print(g) # {1, 2}, 1 -> 2
