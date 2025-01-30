import matplotlib.pyplot as plt
import numpy as np
import csv

ns = []
lg_ts = []

with open('benches/lg_time.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        n, t = row
        ns.append(int(n))
        lg_ts.append(float(t))

nx_ts = []

with open('benches/nx_time.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        _, t = row
        nx_ts.append(float(t))

scg_ts = []

with open('benches/scg_time.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        _, t = row
        scg_ts.append(float(t))

plt.title("Algorytm dijkstry - Czas wykonania")

plt.ylabel("Czas[s]", rotation=0, loc="top")
plt.xlabel("Ilość wykonań", loc="right", labelpad=15)

plt.plot(ns, lg_ts, label="libgraphy")
plt.plot(ns, nx_ts, label="NetworkX")
plt.plot(ns, scg_ts, label="SciPy CSGraph")
plt.legend()

plt.show()

# ********* cpu usage *********
lg_cpus = []
lg_mems = []

with open('benches/lg_cpu_mem.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        _, cpu, mem = row
        lg_cpus.append(float(cpu))
        lg_mems.append(float(mem))

nx_cpus = []
nx_mems = []

with open('benches/nx_cpu_mem.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        _, cpu, mem = row
        nx_cpus.append(float(cpu))
        nx_mems.append(float(mem))

scg_cpus = []
scg_mems = []

with open('benches/scg_cpu_mem.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        _, cpu, mem = row
        scg_cpus.append(float(cpu))
        scg_mems.append(float(mem))


plt.title("Algorytm dijkstry - Użycie CPU")

plt.ylabel("Użycie CPU [%]", rotation=0, loc="top")
plt.xlabel("Ilość wykonań", loc="right", labelpad=15)

plt.plot(ns, lg_cpus, label="libgraphy")
plt.plot(ns, nx_cpus, label="NetworkX")
plt.plot(ns, scg_cpus, label="SciPy CSGraph")
plt.legend()

plt.show()

plt.title("Algorytm dijkstry - Zużycie pamięci RAM")

plt.ylabel("Zużycie RAM [%]", rotation=0, loc="top")
plt.xlabel("Ilość wykonań", loc="right", labelpad=15)

plt.plot(ns, lg_mems, label="libgraphy")
plt.plot(ns, nx_mems, label="NetworkX")
plt.plot(ns, scg_mems, label="SciPy CSGraph")
plt.legend()

plt.show()
