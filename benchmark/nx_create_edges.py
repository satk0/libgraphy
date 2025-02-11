import sys
import json
import networkx as nx

edges = json.loads(sys.argv[1])

n = 50

G = nx.DiGraph()

for i in range(n):
    G.add_node(i)

for e in edges:
    G.add_edge(e[0], e[1], weight=e[2])
