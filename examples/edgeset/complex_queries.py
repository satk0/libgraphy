from libgraphy import GraphFactory, Edge, EdgeSet, MatrixType

# Generate a graph for testing purposes
my_graph = GraphFactory.digraph(10, 5, True)

# Get vertices
vertices = my_graph.edges.vertices

# Get all edges starting at vertex 0
subset1 = my_graph.edges.start_at(vertices[0])

# Get all edges ending at vertex 2
subset2 = my_graph.edges.end_at(vertices[2])

# Get all edges which have values greater than 0.1
subset3 = my_graph.edges > 0.1

# Set value of all edges
my_graph.edges = 1

# Multiply value of all edges
my_graph.edges *= 5

# Reverse all edges in a directed graph
my_graph.edges.reverse(True)

# Get adjacency matrix
adjacency_matrix = my_graph.edges.adjacency_matrix()

# Get incidence matrix
incidence_matrix = my_graph.edges.incidence_matrix()

# Perform a transformation of each edge in a set
def f(e: Edge) -> Edge:
	result = Edge(e.predecessor, e.successor, e.value * 2)
	return result
my_graph.edges.transform(f)