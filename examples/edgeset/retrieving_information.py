from libgraphy import GraphFactory, Edge, EdgeSet

# Generate a graph for testing purposes
my_graph = GraphFactory.petersen()

# Create helper variables
tmp_edge = my_graph.edges[2]
v0 = my_graph.vertices[0]
v2 = my_graph.vertices[2]
nonexistent_edge = Edge(v0, v0)

# Get edge by index in set
print(tmp_edge) # prints "'v0' -> 'v4' = 1"

# Check if the set contains a particular edge
print(tmp_edge in my_graph.edges)  # prints 'True'
print(nonexistent_edge in my_graph.edges) # prints 'False'

# Iterate through all edges in the set
for e in my_graph.edges:
	print(e)

# Get edges by vertex
print(my_graph.edges[v0]) # prints all edges starting at vertex v0

# Get edges by vertex name
print(my_graph.edges["v0"]) # prints the same result as previously

# Get edges by edge
print(my_graph.edges[tmp_edge]) # prints "'v0' -> 'v4' = 1"

# Get edges by tupple
print(my_graph.edges[(v0, v2)])  # prints "'v0' -> 'v1' = 1"

# Get edge by chaining set with subset
print(my_graph.edges[v0][v2]) # prints "'v0' -> 'v1' = 1"

