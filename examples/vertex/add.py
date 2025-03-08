from libgraphy import Vertex

v0 = Vertex("v0")
v1 = Vertex("v1")

v2 = v0 + v1

for n in v2:
    print(n) # v1
