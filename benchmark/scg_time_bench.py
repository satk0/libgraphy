import numpy as np
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import csr_matrix

import csv
from time import time

adjacency_matrix = np.array([
 # s, t,  x, y, z
  [0, 10, 0, 5, 0], # s
  [0, 0 , 1, 2, 0], # t
  [0, 0 , 0, 0, 4], # x
  [0, 3 , 9, 0, 2], # y
  [7, 0 , 6, 0, 0]  # z
])

graph = csr_matrix(adjacency_matrix)

with open('scg_time.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    for n in range(100000, 1000001, 100000):
        start = time()
        for _ in range(n):
            dijkstra(graph, indices=0, directed=True)
        end = time()

        tm = end - start
        print(n, tm)
        csvwriter.writerow([n, tm])

