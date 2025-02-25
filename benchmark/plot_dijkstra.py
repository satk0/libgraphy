import json
import matplotlib.pyplot as plt
import numpy as np

# TODO: print in latex
# plt.rcParams.update({
#     "text.usetex": True,
#     "font.family": "Helvetica"
# })

# Number of repetitive runs of the benchmark
RUNS = 10
NUM_OF_GRAPHS=20

num_of_vertices = [i for i in range(10, NUM_OF_GRAPHS * 10 + 1, 10)]

def create_lists() -> list:
    lg_times = []
    nx_times = []
    scg_times = []

    fname = f'res/dijkstra/dijkstra_times_0.txt'

    with open(fname) as f:
        for l in f:
            _, _, lg_tm, nx_tm, scg_tm = json.loads(l)

            lg_times.append(lg_tm)
            nx_times.append(nx_tm)
            scg_times.append(scg_tm)

    return [lg_times, nx_times, scg_times]

def average_all_runs(lg_times: list, nx_times: list, scg_times: list):
    # summarize
    for i in range(1, RUNS):
        with open(f'res/dijkstra/dijkstra_times_{i}.txt') as f:
            k = 0
            for l in f:
                _, _, lg_tm, nx_tm, scg_tm = json.loads(l)

                lg_times[k] += lg_tm
                nx_times[k] += nx_tm
                scg_times[k] += scg_tm
                k += 1

    # average
    for i in range(len(lg_times)):
        lg_times[i] /= RUNS
        nx_times[i] /= RUNS
        scg_times[i] /= RUNS

    return [lg_times, nx_times, scg_times]

lg_times, nx_times, scg_times = create_lists()
lg_times, nx_times, scg_times = average_all_runs(lg_times, nx_times, scg_times)

print(num_of_vertices)

print('****** LIBGRAPHY ******')
print(lg_times)

print('****** NETWORKX ******')
print(nx_times)

print('****** CSGraph ******')
print(scg_times)

# *** BAR PLOT ***

barWidth = 0.25

IT = [12, 30, 1, 8, 22] 
ECE = [28, 6, 16, 5, 10] 
CSE = [29, 3, 24, 25, 17] 

br1 = np.arange(NUM_OF_GRAPHS)
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

plt.title("Algorytm Dijkstry - Czas")

plt.bar(br1, lg_times, color ='dodgerblue', width = barWidth,
        label ='Libgraphy') 
plt.bar(br2, nx_times, color ='yellowgreen', width = barWidth, 
        label ='NetworkX') 
plt.bar(br3, scg_times, color ='goldenrod', width = barWidth, 
        label ='SciPy') 

plt.xlabel('Graf', loc="right", labelpad=5)
plt.ylabel('Czas [s]', rotation=0, loc="top")

plt.xticks([r + barWidth for r in range(NUM_OF_GRAPHS)], 
        [str(i+1) for i in range(20)])

plt.legend()

# ******


plt.savefig('figures/dijkstra-times.png', bbox_inches='tight')
plt.close()

