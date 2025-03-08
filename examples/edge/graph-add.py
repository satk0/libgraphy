from libgraphy import Graph, Edge

g = Graph()
e = Edge("1", "2")

f = g + e

print(g) # {}
print(f) # {1, 2}, 1 -> 2
