from libgraphy import Vertex

v0 = Vertex("v0")
v1 = Vertex("v1")
v2 = Vertex("v2")

v0 += v1
v0 += v2

for n in v0:
    print(n) # v1, v2
