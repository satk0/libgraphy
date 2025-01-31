import unittest
import pytest
from libgraphy import Route, Edge, Graph
#from libgraphy.exception import LibgraphyError

class TestRoute(unittest.TestCase):

    def test__getitem__(self):
        r = Route(Graph())
        r.edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]

        e1 = r[1]
        assert e1.predecessor.name == '2' and e1.successor.name == '3' \
                and e1.value == 3.4

        e3 = r[3]
        assert e3.predecessor.name == '4' and e3.successor.name == '5' \
                and e3.value == 1.4

    def test__imul__(self):
        g = Graph()
        r = Route(g)
        edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]
        r.edges = edges 
        r *= 9.7

        for i in range(len(r.edges)):
            e = edges[i]
            re = r.edges[i]
            assert re.predecessor.name == e.predecessor.name
            assert re.successor.name == e.successor.name
            assert re.value == 9.7 * e.value
        assert r.graph is g

    def test__mul__(self):
        g = Graph()
        r = Route(g)
        r.edges = [
          Edge("1", "2", 10), Edge("2", "3", 3.4),
          Edge("3", "4", 34), Edge("4", "5", 1.4),
        ]

        nr = 3.24 * r

        for i in range(len(nr.edges)):
            nre = nr.edges[i]
            re = r.edges[i]
            assert nre.predecessor.name == re.predecessor.name
            assert nre.successor.name == re.successor.name
            assert nre.value == 3.24 * re.value

        assert r.graph is g
        assert nr.graph is not g
