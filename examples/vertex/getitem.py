from libgraphy import Vertex

v = Vertex("v")

for i in range(10):
    v += Vertex(i)

print(v[3]) # 3
