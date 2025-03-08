from libgraphy import Vertex

v = Vertex("v")

for i in range(7):
    v += Vertex(i)

del v[4]

for n in v:
    print(n) # 0, 1, 2, 3, 5, 6
