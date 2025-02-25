import os
from enum import Enum

import matplotlib.pyplot as plt

# TODO: print in latex
# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "Helvetica"
# })

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
    cycles_list = []
    instructions_list = []
    sub_name = bench.value + '_50' if bench == Benchmark.EDGES else bench.value
    fname = f'res/{bench.value}_perf/{lib.value}_{sub_name}_0.txt'

    with open(fname) as f:
        for l in f:
            cycles, ins = l.split(',')
            cycles = int(cycles)
            ins = int(ins)

            cycles_list.append(cycles)
            instructions_list.append(ins)

    return [cycles_list, instructions_list]

def average_all_runs(lib: Library, cycles_list: list, instructions_list: list, bench: Benchmark = Benchmark.VERTICES):
    # summarize
    sub_name = bench.value + '_50' if bench == Benchmark.EDGES else bench.value
    for i in range(1, RUNS):
        with open(f'res/{bench.value}_perf/{lib.value}_{sub_name}_{i}.txt') as f:
            k = 0
            for l in f:
                cycles, ins= l.split(',')
                cycles = int(cycles)
                ins = int(ins)

                cycles_list[k] += cycles
                instructions_list[k] += ins
                k += 1

    # average
    for i in range(len(cycles_list)):
        cycles_list[i] /= RUNS
        instructions_list[i] /= RUNS

# ****** VERTICES ******

lg_cycles, lg_instructions = create_lists(Library.LIBGRAPHY)
average_all_runs(Library.LIBGRAPHY, lg_cycles, lg_instructions)

nx_cycles, nx_instructions = create_lists(Library.NETWORKX)
average_all_runs(Library.NETWORKX, nx_cycles, nx_instructions)

scg_cycles, scg_instructions = create_lists(Library.CSGRAPH)
average_all_runs(Library.CSGRAPH, scg_cycles, scg_instructions)

print(num_of_vertices)

print('****** LIBGRAPHY ******')
print(lg_cycles)
print(lg_instructions)

print('****** NETWORKX ******')
print(nx_cycles)
print(nx_instructions)

print('****** CSGraph ******')
print(scg_cycles)
print(scg_instructions)

# ****** Graphs ******

# **** CYCLES ****
plt.title("Tworzenie grafu z wierzchołków - Cykle CPU")

plt.ylabel("Cykle", rotation=0, loc="top")
plt.xlabel("Liczba wierzchołków", loc="right", labelpad=5)

plt.plot(num_of_vertices, lg_cycles, label="Libgraphy")
plt.plot(num_of_vertices, scg_cycles, label="SciPy CSGraph")
plt.plot(num_of_vertices, nx_cycles, label="NetworkX")
plt.legend()


plt.savefig('figures/vertices-cycles.png', bbox_inches='tight')
plt.close()

# **** INSTRUCTIONS ****
plt.title("Tworzenie grafu z wierzchołków - instrukcje CPU")

plt.ylabel("Instrukcje", rotation=0, loc="top")
plt.xlabel("Liczba wierzchołków", loc="right", labelpad=5)

plt.plot(num_of_vertices, lg_instructions, label="Libgraphy")
plt.plot(num_of_vertices, scg_instructions, label="SciPy CSGraph")
plt.plot(num_of_vertices, nx_instructions, label="NetworkX")
plt.legend()

plt.savefig('figures/vertices-instructions.png', bbox_inches='tight')
plt.close()


# ******* EDGES *******

n = 50
num_of_edges_set = [nedges for nedges in range(50, n*(n-1) + 1, 50)]

lg_cycles, lg_instructions = create_lists(Library.LIBGRAPHY, Benchmark.EDGES)
average_all_runs(Library.LIBGRAPHY, lg_instructions, lg_instructions, Benchmark.EDGES)

nx_cycles, nx_instructions = create_lists(Library.NETWORKX, Benchmark.EDGES)
average_all_runs(Library.NETWORKX, nx_instructions, nx_instructions, Benchmark.EDGES)

scg_cycles, scg_instructions = create_lists(Library.CSGRAPH, Benchmark.EDGES)
average_all_runs(Library.CSGRAPH, scg_instructions, scg_instructions, Benchmark.EDGES)

print(num_of_edges_set)

print('****** LIBGRAPHY ******')
print(lg_cycles)
print(lg_instructions)

print('****** NETWORKX ******')
print(nx_cycles)
print(nx_instructions)

print('****** CSGraph ******')
print(scg_cycles)
print(scg_instructions)

# ****** Graphs ******

# **** CYCLES ****
plt.title("Tworzenie grafu z krawędzi - Cykle CPU")

plt.ylabel("Cykle", rotation=0, loc="top")
plt.xlabel("Liczba krawędzi", loc="right", labelpad=5)

plt.plot(num_of_edges_set, lg_cycles, label="Libgraphy")
plt.plot(num_of_edges_set, scg_cycles, label="SciPy CSGraph")
plt.plot(num_of_edges_set, nx_cycles, label="NetworkX")
plt.legend()

plt.savefig('figures/edges-cycles.png', bbox_inches='tight')
plt.close()

# **** INSTRUCTIONS ****
plt.title("Tworzenie grafu z krawędzi - Instrukcje CPU")

plt.ylabel("Instrukcje", rotation=0, loc="top")
plt.xlabel("Liczba krawędzi", loc="right", labelpad=5)

plt.plot(num_of_edges_set, lg_instructions, label="Libgraphy")
plt.plot(num_of_edges_set, scg_instructions, label="SciPy CSGraph")
plt.plot(num_of_edges_set, nx_instructions, label="NetworkX")
plt.legend()

plt.savefig('figures/edges-instructions.png', bbox_inches='tight')
plt.close()

