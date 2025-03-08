from libgraphy import Vertex, Edge

v0 = Vertex(0)
v1 = Vertex(1)

e0 = Edge(v0, v1)
e1 = Edge("1", "2")

print(e0.predecessor, e0.successor) # 0, 1
print(e1.predecessor, e1.successor) # 1, 2
