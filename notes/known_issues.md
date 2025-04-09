# Known issues and ideas (that hurt me but are low priority):
* [ ] make libgraphy **as strict as possible**
* [ ] v1(g: None) += v2(g: None) -> g1(g: nG) & g2(g: nG), nG - new graph
* [ ] e = Edge(v1(g: G), v2(g: None)) -> e(g: G) & v2(g:G)
* [ ] e = Edge(v1(g: None), v2(g: None)) -> e(g: nG) & v2(g: nG)
* [ ] make - e = Edge(v1: Vertex, v2: str) (and other way around) - work
* [ ] make e.precedessor|successor, path.edges, graph.edges, vertices etc. **read only**
* [ ] cascade delete graph edges when del vertex
* [ ] cascade delete graph edges and vertices when del graph (deleting edge does not change anything)
