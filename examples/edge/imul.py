from libgraphy import Edge

e = Edge("1", "2", 4)
e *= 4

print(e.value) # 16
