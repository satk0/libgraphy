from libgraphy import Graph, Vertex, Edge, AlgorithmEnum

g = Graph()
for i in range(10):
    g += Vertex(i)

for i in range(0, len(g.vertices)-1):
    p, s = g.vertices[i], g.vertices[i+1]
    g += Edge(p, s, i+1)

path = g.find_path(g.vertices[0], g.vertices[-1], algorithm = AlgorithmEnum.DIJKSTRA)
new_path = path * 3.14

print(path.value, new_path.value) # 45, 141.3
