from libgraphy import Vertex

v0 = Vertex("v0")

for i in range(1, 5):
    v0 += Vertex(i) # 1, 2, 3, 4

for n in v0:
    print(n) # 1, 2, 3, 4
