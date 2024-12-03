import threading
import psutil
from libgraphy import *

def display_cpu():
    global running

    running = True

    currentProcess = psutil.Process()

    # start loop
    while running:
        print("cpu usage:", currentProcess.cpu_percent(interval=0.1))
        print("virtual memory:", currentProcess.memory_info())

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

start()
try:
    for i in range(10000):
        route: Route = g.findPath(AlgorithmEnum.DJIKSTRA, s, x)
finally: # stop thread even if I press Ctrl+C
    stop()

