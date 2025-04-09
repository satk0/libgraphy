from libgraphy import Graph, Vertex, Edge, AlgorithmEnum

g = Graph()
for i in range(10):
    g += Vertex(i)

for i in range(0, len(g.vertices)-1):
    p, s = g.vertices[i], g.vertices[i+1]
    g += Edge(p, s, i+1)

path = g.findPath(AlgorithmEnum.DIJKSTRA, g.vertices[0], g.vertices[-1])

e = path[-1]
print(e.predecessor, e.successor) # 8, 9
