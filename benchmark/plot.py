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

class Benchmark(Enum):
    VERTICES = 'vertices'
    EDGES = 'edges'
    DIJKSTRA = 'dijkstra' # TODO: implement


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

def create_lists(lib: Library, bench: Benchmark = Benchmark.VERTICES) -> list:
    times_list = []
    cpus_list = []
    mems_list = []
    sub_name = bench.value + '_50' if bench == Benchmark.EDGES else bench.value
    fname = f'res/{bench.value}/{lib.value}_{sub_name}_0.txt'

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

def average_all_runs(lib: Library, times_list: list, mems_list: list, cpus_list: list, bench: Benchmark = Benchmark.VERTICES):
    # summarize
    sub_name = bench.value + '_50' if bench == Benchmark.EDGES else bench.value
    for i in range(1, RUNS):
        with open(f'res/{bench.value}/{lib.value}_{sub_name}_{i}.txt') as f:
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
    for i in range(len(times_list)):
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

# ****** Graphs ******

# **** TIME ****
plt.title("Tworzenie grafu z wierzchołków - Czas")

plt.ylabel("Czas [ms]", rotation=0, loc="top")
plt.xlabel("Liczba wierzchołków", loc="right", labelpad=5)

plt.plot(num_of_vertices, lg_times, label="Libgraphy")
plt.plot(num_of_vertices, scg_times, label="SciPy CSGraph")
plt.plot(num_of_vertices, nx_times, label="NetworkX")
plt.legend()


plt.savefig('figures/vertices-time.png', bbox_inches='tight')
plt.close()

# **** MEMORY ****
plt.title("Tworzenie grafu z wierzchołków - Pamięć RAM")

plt.ylabel("Maks. RAM [KB]", rotation=0, loc="top")
plt.xlabel("Liczba wierzchołków", loc="right", labelpad=5)

plt.plot(num_of_vertices, lg_mems, label="Libgraphy")
plt.plot(num_of_vertices, scg_mems, label="SciPy CSGraph")
plt.plot(num_of_vertices, nx_mems, label="NetworkX")
plt.legend()

plt.savefig('figures/vertices-memory.png', bbox_inches='tight')
plt.close()

# **** CPU ****
plt.title("Tworzenie grafu z wierzchołków - Zużycie CPU")

plt.ylabel("CPU [%]", rotation=0, loc="top")
plt.xlabel("Liczba wierzchołków", loc="right", labelpad=5)

plt.plot(num_of_vertices, lg_cpus, label="Libgraphy")
plt.plot(num_of_vertices, scg_cpus, label="SciPy CSGraph")
plt.plot(num_of_vertices, nx_cpus, label="NetworkX")
plt.legend()

plt.savefig('figures/vertices-cpu.png', bbox_inches='tight')
plt.close()

# ******* EDGES *******

n = 50
num_of_edges_set = [nedges for nedges in range(50, n*(n-1) + 1, 50)]

lg_times, lg_mems, lg_cpus = create_lists(Library.LIBGRAPHY, Benchmark.EDGES)
average_all_runs(Library.LIBGRAPHY, lg_times, lg_mems, lg_cpus, Benchmark.EDGES)

nx_times, nx_mems, nx_cpus = create_lists(Library.NETWORKX, Benchmark.EDGES)
average_all_runs(Library.NETWORKX, nx_times, nx_mems, nx_cpus, Benchmark.EDGES)

scg_times, scg_mems, scg_cpus = create_lists(Library.CSGRAPH, Benchmark.EDGES)
average_all_runs(Library.CSGRAPH, scg_times, scg_mems, scg_cpus, Benchmark.EDGES)

print(num_of_edges_set)

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

# ****** Graphs ******

# **** TIME ****
plt.title("Tworzenie grafu z krawędzi - Czas")

plt.ylabel("Czas [ms]", rotation=0, loc="top")
plt.xlabel("Liczba krawędzi", loc="right", labelpad=5)

plt.plot(num_of_edges_set, lg_times, label="Libgraphy")
plt.plot(num_of_edges_set, scg_times, label="SciPy CSGraph")
plt.plot(num_of_edges_set, nx_times, label="NetworkX")
plt.legend()

plt.savefig('figures/edges-time.png', bbox_inches='tight')
plt.close()

# **** MEMORY ****
plt.title("Tworzenie grafu z krawędzi - Pamięć RAM")

plt.ylabel("Maks. RAM [KB]", rotation=0, loc="top")
plt.xlabel("Liczba krawędzi", loc="right", labelpad=5)

plt.plot(num_of_edges_set, lg_mems, label="Libgraphy")
plt.plot(num_of_edges_set, scg_mems, label="SciPy CSGraph")
plt.plot(num_of_edges_set, nx_mems, label="NetworkX")
plt.legend()

plt.savefig('figures/edges-memory.png', bbox_inches='tight')
plt.close()

# **** CPU ****
plt.title("Tworzenie grafu z krawędzi - Zużycie CPU")

plt.ylabel("CPU [%]", rotation=0, loc="top")
plt.xlabel("Liczba krawędzi", loc="right", labelpad=5)

plt.plot(num_of_edges_set, lg_cpus, label="Libgraphy")
plt.plot(num_of_edges_set, scg_cpus, label="SciPy CSGraph")
plt.plot(num_of_edges_set, nx_cpus, label="NetworkX")
plt.legend()

plt.savefig('figures/edges-cpu.png', bbox_inches='tight')
plt.close()

