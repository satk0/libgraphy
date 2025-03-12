from libgraphy import Graph, Vertex, Edge, AlgorithmEnum

g = Graph()
for i in range(10):
    g += Vertex(i)

for i in range(0, len(g.vertices)-1):
    p, s = g.vertices[i], g.vertices[i+1]
    g += Edge(p, s, i+1)

route = g.findPath(AlgorithmEnum.DIJKSTRA, g.vertices[0], g.vertices[-1])
route *= 8
print(route.value) # 45
