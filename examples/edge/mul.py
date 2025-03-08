from libgraphy import Edge

e0 = Edge("1", "2", 4)
e1 = e0 * 3
e2 = 2 * e1

print(e0.value, e1.value, e2.value) # 4, 12, 24
