from libgraphy import Vertex, Graph

a = Vertex("a")
neighbors = ["2", "3", "4", "5"]

g = Graph()

for n in neighbors:
    a += Vertex(n)

g += a
for n in a:
    g += n

print(g) # w_a2 = 1; w_a3 = 1; w_a4 = 1; w_a5 = 1;
