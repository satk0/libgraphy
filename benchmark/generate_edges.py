# import argparse
import random


'''
CLI=argparse.ArgumentParser(prog='Edges generator',
                            description='Generates e distinct edges\
                            with n vertices')
CLI.add_argument(
  "-e",
  type=int,
  help='Number of edges'
)

CLI.add_argument(
  "-n",
  type=int,
  help='Number of vertices'
)

args = CLI.parse_args()

e = args.e
n = args.n
'''
n = 50

# if n * (n-1) < e:
#     raise Exception("Not enough vertices")

vertices = [v for v in range(n)]
list_of_edges = []

def in_edges(v1, v2, edges) -> bool:
    for e in edges:
        if v1 is e[0] and v2 is e[1]:
            return True
    return False

print("1. Generating edges...")

for no_edges in range(50, n*(n-1) + 1, 50):
    edges = []
    for _ in range(no_edges):
        appended = False

        while not appended:
            v1 = random.choice(vertices)
            v2 = random.choice(vertices)
            value = random.randint(-100, 100)

            #if v1 != v2 and [v1, v2, value] not in edges:
            if v1 != v2 and not in_edges(v1, v2, edges):
                edges.append([v1, v2, value])
                appended = True

    list_of_edges.append(edges)

fname = "generated/edges_50.txt"
print(f"2. Writing edges to '{fname}' file...")

with open(fname, 'w+') as f:
    for edges in list_of_edges:
        f.write(f"{edges}\n")

print("Done.")
