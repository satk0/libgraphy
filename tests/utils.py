from libgraphy import *

def assert_compare_graph_values(g: Graph, f: Graph):
    assert len(g.vertices) == len(f.vertices) and \
            len(g.edges) == len(f.edges)

    for i in range(len(g.vertices)):
        vg, vf = g.vertices[i], f.vertices[i]
        assert vg.name == vf.name and vg.value == vf.value

        assert len(vg.neighbors) == len(vf.neighbors) and \
               len(vg.adjacent_edges) == len(vf.adjacent_edges)

        for j in range(len(vg.neighbors)):
            vgn, vfn = vg.neighbors[j], vf.neighbors[j]
            assert vgn.name == vfn.name and vgn.value == vfn.value

        for j in range(len(vg.adjacent_edges)):
            aeg, aef = vg.adjacent_edges[j], vf.adjacent_edges[j]
            assert aeg.predecessor.name == aef.predecessor.name and \
                aeg.predecessor.value == aef.predecessor.value and \
                aeg.successor.name == aef.successor.name and \
                aeg.successor.value == aef.successor.value

def create_test_graph() -> Graph:
    # Example comes from "Introduction to Algorithms" (Fourth Edition) Figure 22.6 - page: 621
    vertices = [Vertex(l) for l in "stxyz"]
    s, t, x, y, z = vertices

    edges = [Edge(s, y, 5), Edge(y, t, 3), Edge(t, x),
             Edge(s, t, 10), Edge(t, y, 2), Edge(y, x, 9),
             Edge(x, z, 4), Edge(z, x, 6), Edge(z, s, 7),
             Edge(y, z, 2)]

    g = Graph()
    for v in vertices:
        g += v

    for e in edges:
        g += e

    return g

# do the same for 6 and 8
def grid_level4_graph() -> Graph:
    '''
    Creates grid graph of level 4:

    0 - 1 - 2
    |   |   |
    7 - 8 - 3
    |   |   |
    6 - 5 - 4
    '''
    g: Graph = Graph()

    for i in range(8):
        g += Vertex(i)

    for i in range(7):
        g += Edge(g.vertices[i], g.vertices[i+1])
        g += Edge(g.vertices[i+1], g.vertices[i])

    g += Edge(g.vertices[-1], g.vertices[0])
    g += Edge(g.vertices[0], g.vertices[-1])

    g += Vertex(8)

    for i in range(1, 8, 2):
        g += Edge(g.vertices[i], g.vertices[-1])
        g += Edge(g.vertices[-1], g.vertices[i])

    return g

def grid_level6_graph() -> Graph:
    g: Graph = Graph()

    for i in range(6):
        g += Vertex(i)
    g += Vertex(6)

    for i in range(5):
        g += Edge(g.vertices[i], g.vertices[i+1])
        g += Edge(g.vertices[i+1], g.vertices[i])
        g += Edge(g.vertices[i], g.vertices[-1])
        g += Edge(g.vertices[-1], g.vertices[i])

    g += Edge(g.vertices[-2], g.vertices[0])
    g += Edge(g.vertices[0], g.vertices[-2])
    g += Edge(g.vertices[-2], g.vertices[-1])
    g += Edge(g.vertices[-1], g.vertices[-2])

    g += Vertex(7)
    g += Edge(g.vertices[-1], g.vertices[4])
    g += Edge(g.vertices[4], g.vertices[-1])
    g += Edge(g.vertices[-1], g.vertices[3])
    g += Edge(g.vertices[3], g.vertices[-1])

    return g


def grid_level8_graph() -> Graph:
    g: Graph = Graph()

    for i in range(8):
        g += Vertex(i)
    g += Vertex(9)

    for i in range(7):
        g += Edge(g.vertices[i], g.vertices[i+1])
        g += Edge(g.vertices[i+1], g.vertices[i])
        g += Edge(g.vertices[i], g.vertices[-1])
        g += Edge(g.vertices[-1], g.vertices[i])

    g += Edge(g.vertices[-2], g.vertices[0])
    g += Edge(g.vertices[0], g.vertices[-2])
    g += Edge(g.vertices[-2], g.vertices[-1])
    g += Edge(g.vertices[-1], g.vertices[-2])

    g += Vertex(10)
    g += Edge(g.vertices[-1], g.vertices[4])
    g += Edge(g.vertices[4], g.vertices[-1])
    g += Edge(g.vertices[-1], g.vertices[3])
    g += Edge(g.vertices[3], g.vertices[-1])

    return g
