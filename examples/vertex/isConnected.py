from libgraphy import Vertex

v1 = Vertex("v1", -23.45)
v2 = Vertex("v2")

v1 += v2

print(v1.isConnected(v2), v2.isConnected(v1))
# True False
