from __future__ import annotations
from .vertex import Vertex
from .edge import Edge
from .exception import LibgraphyError
from .utils import EdgeOverrideMode

from typing import Optional, Self, Any, TYPE_CHECKING, override

if TYPE_CHECKING:  # pragma: no cover
	from .graph import Graph

from copy import deepcopy
from random import randint

__all__ = ["EdgeSet"]

class EdgeSet():
	def __init__(self, reference: Optional[EdgeSet|list[Edge]] = None, graph: Optional[Graph] = None) -> None:
		# Basic initialization
		self.graph: Optional[Graph] = graph
		self.__container = dict()
		self.__size = 0
		
		# If reference supplied
		if reference is not None:
			if isinstance(reference, EdgeSet):
				for starting_vertex, subset in reference.__container.items():
					if starting_vertex not in self.__container:
						self.__container[starting_vertex] = dict()
					for ending_vertex, edge in subset.items():
						self.__container[starting_vertex][ending_vertex] = edge
					self.__size += len(self.__container[starting_vertex])
					
			elif isinstance(reference, list):
				if len(reference) > 0:
					self.graph = reference[0].graph
				self.__size = len(reference)
				for edge in reference:
					if not isinstance(reference[edge], Edge):
						raise LibgraphyError(f"Unsupported argument type for 'reference'. List contains element of"
						                     f" type {type(reference[edge])}")
					if edge.predecessor not in self.__container:
						self.__container[edge.predecessor] = dict()
					self.__container[edge.predecessor][edge.successor] = edge
					
	def start_at(self, start_vertex: Vertex) -> EdgeSet:
		subset = EdgeSet()
		if start_vertex in self.__container.keys():
			subset.__container[start_vertex] = self.__container[start_vertex]
			subset.__size = len(self.__container[start_vertex])
		return subset
	
	def end_at(self, end_vertex: Vertex) -> EdgeSet:
		subset = EdgeSet()
		for starting_vertex, ending_vertices_list in self.__container.items():
			if end_vertex in ending_vertices_list.keys():
				subset.__container[starting_vertex] = dict()
				subset.__container[starting_vertex][end_vertex] = self.__container[starting_vertex][end_vertex]
				subset.__size += 1
		return subset
	
	def reverse(self, override: bool = False) -> EdgeSet:
		newContainer = dict()
		for starting_vertex, subset in self.__container.items():
			for ending_vertex, edge in subset.items():
				if ending_vertex not in newContainer:
					newContainer[ending_vertex] = dict()
				newContainer[ending_vertex][starting_vertex] = edge.reverse(override)
		self.__container = newContainer
		return self
	
	def __getitem__(self, key: tuple|Vertex|Edge|int|str) -> Edge|EdgeSet|None:
		# Handle tuple in the form of (starting_vertex, ending_vertex)
		if isinstance(key, tuple):
			if key[0] in self.__container:
				if key[1] in self.__container[key[0]]:
					return self.__container[key[0]][key[1]]
			return None
		
		# Handle actual Edge object
		elif isinstance(key, Edge):
			if key.predecessor in self.__container:
				if key.successor in self.__container[key.predecessor]:
					return self.__container[key.predecessor][key.successor]
			return None
		
		elif isinstance(key, str):
			return self.by_vertex_name(key)
		
		# Handle index
		elif isinstance(key, int):
			if key>=0:
				combined_index = 0
				for starting_vertex, subset in self.__container.items():
					if combined_index + len(subset) > key:
						return self.__container[starting_vertex][list(self.__container[starting_vertex])[key-combined_index]]
					combined_index += len(subset)
				return None
			else:
				#TODO: handle negative keys
				pass
		
		elif isinstance(key, Vertex):
			if key in self.__container.keys():
				subset = EdgeSubSet(origin = key)
				subset.__container[key] = self.__container[key]
				return subset
			else:
				return None
		
		# Fail
		else:
			raise LibgraphyError(f"Unknown indexing type: {type(key)}. Edge set can be iterated only using tuples,"
			                     f" indices, strings, Edge, and Vertex objects")
	
	def by_vertex_name(self, vertex_name: str) -> EdgeSet:
		subset = EdgeSet()
		for v in self.__container.keys():
			if v.name == vertex_name:
				subset.__container[v] = self.__container[v]
				subset.__size += len(self.__container[v])
		return subset
	
	def __setitem__(self, key: Any, value: Any) -> None:
		if isinstance(value, Edge):
			edge = self[key]
			
			# Remove edge if already present
			if edge is not None:
				self.remove(edge)
			
			# Add new edge
			self.append(value)
		else:
			self.set_value(key, value)
	
	def set_value(self, key: Any, value: Any) -> EdgeSet:
		# Sanity checks
		if isinstance(key, Vertex):
			if not isinstance(value, EdgeSet) and not isinstance(value, list) and not isinstance(value, Vertex):
				raise LibgraphyError(
					f"Unsupported argument combination. When iterating over EdgeSet by vertices, value needs to be of"
					f" either EdgeSet, Vertex or list(Vertex) type ({type(value)} supplied)")
			if key not in self.__container:
				self.__container[key] = dict()
			
			if isinstance(value, Vertex):
				if value not in self.__container[key]:
					self.__size += 1
				self.__container[key][value] = Edge(key, value, 1)
			elif isinstance(value, EdgeSet):
				if value.graph != self.graph:
					if self.graph is None:
						self.graph = value.graph
					elif value.graph is not None:
						raise LibgraphyError(f"Cannot add EdgeSet to EdgeSet, as sets belong to different graphs")
				for e in value:
					if e.predecessor == key:
						self.append(e)
			elif isinstance(list):
				for v in list:
					if not isinstance(v, Vertex):
						raise LibgraphyError(f"Unsupported argument combination. When iterating over EdgeSet by"
						                     f" vertices, value needs to be of either EdgeSet, Vertex or list(Vertex)"
						                     f" type ({type(v)} supplied as list element)")
					if v not in self.__container[key]:
						self.__container[key][v] = 1
						self.__size += 1
		
		# Try retrieving edge
		edge = self[key]
		
		# Set value if edge already present
		if edge is not None:
			edge.value = value
			return self
		
		# Otherwise, create new edge and set its value
		if isinstance(key, tuple):
			self.append(Edge(key[0], key[1], value))
		elif isinstance(key, Edge):
			if key.graph != self.graph:
				if self.graph is None:
					self.graph = key.graph
				elif key.graph is None:
					key.graph = self.graph
				else:
					raise LibgraphyError(f"Edge already belongs to a different graph")
			key.value = value
			self.append(key)
		else:
			raise LibgraphyError(f"Unsupported argument type for 'key': {type(key)} supplied")
		return self
	
	def __iadd__(self, other: Edge|EdgeSet) -> EdgeSet:
		if isinstance(other, Edge):
			self.append(other)
		elif isinstance(other, EdgeSet):
			self.extend(other)
		else:
			raise LibgraphyError(f"Unsupported argument type for 'other'. Must be Edge or EdgeSet,"
			                     f" {type(other)} supplied")
		return self
	
	def __add__(self, other: Edge|EdgeSet) -> EdgeSet:
		newSet = EdgeSet(self)
		newSet += other
		return newSet
	
	def append(self, value: Edge) -> None:
		# Sanity checks
		if not isinstance(value, Edge):
			raise LibgraphyError(f"Unsupported argument type for 'value'. Must be Edge, {type(value)} supplied")
		if value.graph != self.graph:
			if self.graph is None:
				self.graph = value.graph
			elif value.graph is None:
				value.graph = self.graph
			else:
				raise LibgraphyError(f"Edge already belongs to a different graph")
		
		# Add Edge
		if value.predecessor not in self.__container:
			self.__container[value.predecessor] = dict()
		self.__container[value.predecessor][value.successor] = value
		self.__size += 1
	
	def extend(self, other: EdgeSet) -> None:
		# Sanity checks
		if not isinstance(other, EdgeSet):
			raise LibgraphyError(f"Unsupported argument type for 'other'. Must be EdgeSet, {type(other)} supplied")
		if other.graph != self.graph:
			if self.graph is None:
				self.graph = other.graph
			elif other.graph is None:
				other.graph = self.graph
			else:
				raise LibgraphyError(f"EdgeSet already belongs to a different graph")
			
		# Add edges to this set
		for starting_vertex, subset in other.__container.items():
			if starting_vertex not in self.__container:
				self.__container[starting_vertex] = dict()
			for ending_vertex, edge in subset.items():
				self.__container[starting_vertex][ending_vertex] = edge
				
		self.__size += other.__size
	
	def __isub__(self, other: Edge | EdgeSet) -> EdgeSet:
		self.remove(other)
		return self
	
	def __sub__(self, other: Edge | EdgeSet) -> EdgeSet:
		newSet = EdgeSet(self)
		newSet -= other
		return newSet

	def __delitem__(self, key: Edge|EdgeSet) -> None:
		self.remove(key)
		
	def remove(self, value: Edge|EdgeSet) -> EdgeSet:
		# Remove edge
		if isinstance(value, Edge):
			if value.predecessor in self.__container and value.successor in self.__container[value.predecessor]:
				del self.__container[value.predecessor][value.successor]
				if len(self.__container[value.predecessor]) == 0:
					del self.__container[value.predecessor]
				self.__size -= 1
				
		# Remove subset
		elif isinstance(value, EdgeSet):
			if self.graph is not None and value.graph is not None\
				and self.graph != value.graph:
					return self
			for starting_vertex, subset in value.__container.items():
				if starting_vertex not in self.__container:
					continue
				for ending_vertex, edge in subset.items():
					if ending_vertex not in self.__container[starting_vertex]:
						continue
					del self.__container[starting_vertex][ending_vertex]
					self.__size -= 1
				if len(self.__container[starting_vertex]) == 0:
					del self.__container[starting_vertex]
					
		# Unsupported type
		else:
			raise LibgraphyError(f"Unsupported argument type for 'value'. Must be Edge or EdgeSet,"
			                     f" {type(value)} supplied")
		
		# Return self
		return self
	
	def __imul__(self, scalar) -> EdgeSet:
		for starting_vertex, subset in self.__container.items():
			for ending_vertex, edge in subset.items():
				self.__container[starting_vertex][ending_vertex].value *= scalar
		return self
		
	def __len__(self) -> int:
		return self.__size
	
	def __contains__(self, item: Edge|tuple) -> bool:
		if isinstance(item, tuple):
			return item[0] in self.__container and item[1] in self.__container[item[0]]
		
		# Handle actual Edge object
		elif isinstance(item, Edge):
			return item.predecessor in self.__container and item.successor in self.__container[item.predecessor]
		
		else:
			raise LibgraphyError(f"Unsupported argument type for 'item'. Must be Edge or tuple, {type(item)} supplied")
	
	def __iter__(self):
		for i in range(self.__size):
			yield self[i]
	
	def __str__(self) -> str:
		desc = "Edges:"
		if self.__container is None or len(self.__container)==0:
			desc += "\n |  None."
		for starting_vertex, subset in self.__container.items():
			desc += f"\n | Vertex: {starting_vertex.name} ({starting_vertex.__repr__()})"
			for ending_vertex, edge in subset.items():
				desc += (f"\n |  | {starting_vertex.name} -> {ending_vertex.name}"
				         f" = {edge.value} ({starting_vertex.__repr__()})")
		return desc
	
	def vertices(self) -> list[Vertex]:
		vertice_list = []
		for starting_vertex, subset in self.__container.items():
			if starting_vertex not in vertice_list:
				vertice_list.append(starting_vertex)
			for ending_vertex in subset.keys():
				if ending_vertex not in vertice_list:
					vertice_list.append(ending_vertex)
		return vertice_list
	
	def incidence_matrix(self) -> list[int][int]:
		# TODO: retrieve a numpy matrix if numpy available
		matrix = dict()
		vertices = self.vertices()
		
		for edge in self:
			matrix[edge] = dict()
			for v in vertices:
				if edge.predecessor == v:
					matrix[edge][v] = 1
				elif edge.successor == v:
					matrix[edge][v] = -1
				else:
					matrix[edge][v] = 0
		return matrix
	
class EdgeSubSet(EdgeSet):
	@override
	def __init__(self, reference: Optional[EdgeSet | list[Edge]] = None, graph: Optional[Graph] = None, origin: Vertex = None) -> None:
		super().__init__(reference, graph)
		self.__origin = origin

	@override
	def __getitem__(self, key: tuple | Vertex | Edge | int | str) -> Edge | EdgeSet | None:
		if isinstance(key, Vertex):
			if key in self._EdgeSet__container[self.__origin].keys():
				return self._EdgeSet__container[self.__origin][key]
			else:
				return None
		else:
			return super().__getitem__(key)
		
	# ********** Graph **********
	# TODO
	#def _graph__iadd__(self, graph: Graph) -> Graph:
	#	for e in self:
	#		graph += e
	#	return graph
	
	#def _graph__add__(self, graph: Graph) -> Graph:
	#	g: Graph = deepcopy(graph)
	#	g += self
	#	return g

# ***************************
