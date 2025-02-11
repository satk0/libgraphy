import sys
import networkx as nx

n = int(sys.argv[1])

G = nx.DiGraph()
for i in range(n):
    G.add_node(i)
