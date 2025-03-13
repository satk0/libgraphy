from libgraphy import Vertex, Graph, Edge

v1 = Vertex()
v2 = Vertex()

g = Graph()
g += v2
g += v1
g += Edge(v1, v2, 10)

print(Graph.to_json(g)) # { "py/object": "libgraphy.graph.Graph", "vertices": ...}
