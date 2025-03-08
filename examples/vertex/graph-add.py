from libgraphy import Vertex, Graph

a = Vertex("a")
g = Graph()

f = g + a

print(g) # {}
print(f) # {a}
