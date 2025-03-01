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

