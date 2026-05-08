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

# Select edges by custom criterions
def is_loop(e: Edge) -> bool:
	return e.predecessor == e.successor

subset4 = my_graph.edges.select(is_loop)

# Perform a simple transformation of each edge in a set
def f(e: Edge) -> Edge:
	e.value *= 2.5
	return e
my_graph.edges.transform(f)

# Perform a complex transformation, using additional arguments
class Counter:
    def __init__(self, start=0):
        self.value = start
	    
    def increment(self):
        current = self.value
        self.value += 3
        return current

def f2(e: Edge, counter: Counter) -> Edge:
	e.value = counter.increment()
	return e

counter = Counter(5)
my_graph.edges.transform(f2, counter)