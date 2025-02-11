import threading
import psutil

import numpy as np
from scipy.sparse.csgraph import dijkstra
from scipy.sparse import csr_matrix

import sys

k = 0
sc = 0
sm = 0

def display_cpu():
    global running
    global sc
    global sm
    global k

    running = True

    currentProcess = psutil.Process()

    # start loop
    while running:
        cpu_usage = currentProcess.cpu_percent(interval=0.1)
        mem_usage = currentProcess.memory_percent()

        sc += cpu_usage
        sm += mem_usage
        k += 1

def start():
    global th

    # create thread and start it
    th = threading.Thread(target=display_cpu)
    th.start()
    
def stop():
    global running
    global th

    # use `running` to stop loop in thread so thread will end
    running = False

    # wait for thread's end
    th.join()

adjacency_matrix = np.array([
 # s, t,  x, y, z
  [0, 10, 0, 5, 0], # s
  [0, 0 , 1, 2, 0], # t
  [0, 0 , 0, 0, 4], # x
  [0, 3 , 9, 0, 2], # y
  [7, 0 , 6, 0, 0]  # z
])

graph = csr_matrix(adjacency_matrix)

n = int(sys.argv[1])

start()
try:
    for i in range(n):
        dijkstra(graph, indices=0, directed=True)
finally: # stop thread even if I press Ctrl+C
    stop()

avgc = sc/k
avgm = sm/k

#print("n | Average CPU usage: | Average memory usage:")
print(f"{n},{avgc},{avgm}")
