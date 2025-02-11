import threading
import psutil
import networkx as nx

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

G = nx.DiGraph()

vertices = [l for l in "stxyz"]
s, t, x, y, z = vertices
edges = [(s, t, 10), (t, y, 2), (y, x, 9),
    (x, z, 4), (z, x, 6), (z, s, 7),
    (y, z, 2), (s, y, 5), (y, t, 3), (t, x, 1)]

for e in edges:
    G.add_edge(e[0], e[1], weight=e[2])

n = int(sys.argv[1])

start()
try:
    for i in range(n):
        nx.dijkstra_path(G, s, x)
finally: # stop thread even if I press Ctrl+C
    stop()

avgc = sc/k
avgm = sm/k

print(f"{n},{avgc},{avgm}")
