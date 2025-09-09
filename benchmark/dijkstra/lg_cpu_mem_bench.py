import threading
import psutil
from libgraphy import *

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
        # https://stackoverflow.com/questions/51571585/psutil-process-cpu-percent-greater-than-100
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

vertices = [Vertex(l) for l in "stxyz"]
s, t, x, y, z = vertices

edges = [Edge(s, t, 10), Edge(t, y, 2), Edge(y, x, 9),
     Edge(x, z, 4), Edge(z, x, 6), Edge(z, s, 7),
     Edge(y, z, 2), Edge(s, y, 5), Edge(y, t, 3), Edge(t, x)]

g = Graph()
for v in vertices:
    g += v

for e in edges:
    g += e

n = int(sys.argv[1])

start()
try:
    for i in range(n):
        g.find_path(s, x, algorithm = AlgorithmEnum.DIJKSTRA)
finally: # stop thread even if I press Ctrl+C
    stop()

avgc = sc/k
avgm = sm/k

print(f"{n},{avgc},{avgm}")
