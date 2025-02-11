import os
from enum import Enum

import matplotlib.pyplot as plt

# Number of repetitive runs of the benchmark
RUNS = 10

num_of_vertices = [i for i in range(5, 101, 5)]

class Library(Enum):
    LIBGRAPHY = 'lg'
    NETWORKX = 'nx'
    CSGRAPH = 'scg'


print(num_of_vertices)


# calculate time in miliseconds
def calc_time(tm: str) -> int:
    hm, ms = tm.split('.')
    min, s = hm.split(':')
    ms = int(ms) * 10
    ms += int(s) * 1000
    ms += int(min) * 60 * 1000

    return ms


def calc_cpu(cpu: str) -> float:
    return float(cpu) / os.cpu_count()

def create_lists(lib: Library) -> list:
    times_list = []
    cpus_list = []
    mems_list = []
    fname = f'res/vertices/{lib.value}_vertices_0.txt'

    with open(fname) as f:
        for l in f:
            mem, cpu, tm = l.split(',')
            cpu = calc_cpu(cpu)
            tm = calc_time(tm)
            mem = int(mem)

            times_list.append(tm)
            cpus_list.append(mem)
            mems_list.append(cpu)

    return [times_list, cpus_list, mems_list]

def average_all_runs(lib: Library, times_list: list, mems_list: list, cpus_list: list):
    # summarize
    for i in range(1, RUNS):
        with open(f'res/vertices/{lib.value}_vertices_{i}.txt') as f:
            k = 0
            for l in f:
                mem, cpu, tm = l.split(',')
                cpu = calc_cpu(cpu)
                tm = calc_time(tm)
                mem = int(mem)

                times_list[k] += tm
                mems_list[k] += mem
                cpus_list[k] += cpu
                k += 1

    # average
    for i in range(len(num_of_vertices)):
        times_list[i] /= RUNS
        mems_list[i] /= RUNS
        cpus_list[i] /= RUNS


lg_times, lg_mems, lg_cpus = create_lists(Library.LIBGRAPHY)
average_all_runs(Library.LIBGRAPHY, lg_times, lg_mems, lg_cpus)

nx_times, nx_mems, nx_cpus = create_lists(Library.NETWORKX)
average_all_runs(Library.NETWORKX, nx_times, nx_mems, nx_cpus)

scg_times, scg_mems, scg_cpus = create_lists(Library.CSGRAPH)
average_all_runs(Library.CSGRAPH, scg_times, scg_mems, scg_cpus)

print(num_of_vertices)

print('****** LIBGRAPHY ******')
print(lg_times)
print(lg_mems)
print(lg_cpus)

print('****** NETWORKX ******')
print(nx_times)
print(nx_mems)
print(nx_cpus)

print('****** CSGraph ******')
print(scg_times)
print(scg_mems)
print(scg_cpus)

plt.title("Tworzenie grafu z wierzchołków - Czas")

plt.ylabel("Czas [ms]", rotation=0, loc="top")
plt.xlabel("Liczba wierzchołków", loc="right", labelpad=15)

plt.plot(num_of_vertices, lg_times, label="libgraphy")
plt.plot(num_of_vertices, nx_times, label="NetworkX")
plt.plot(num_of_vertices, scg_times, label="SciPy CSGraph")
plt.legend()

plt.show()
