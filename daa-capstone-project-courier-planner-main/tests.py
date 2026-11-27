import unittest
from sorting import merge_sort, insertion_sort
from knapsack import knapsack
from graph import dijkstra, nearest_neighbour_route
from utils import generate_parcels

G = {"A": {"B": 1, "C": 4}, "B": {"A": 1, "C": 2, "D": 6}, "C": {"A": 4, "B": 2, "D": 3}, "D": {"B": 6, "C": 3}}

class T(unittest.TestCase):
    def test_sorts_agree(self):
        ps = generate_parcels(60, ["X"], seed=3)
        self.assertEqual(merge_sort(ps), insertion_sort(ps))
    def test_knapsack(self):
        ps = [{"weight": 1, "priority": 1}, {"weight": 3, "priority": 4}, {"weight": 4, "priority": 5}, {"weight": 5, "priority": 7}]
        v, _, _ = knapsack(ps, 7); self.assertEqual(v, 9)
    def test_dijkstra(self):
        d, _ = dijkstra(G, "A"); self.assertEqual(d["D"], 6)
    def test_route(self):
        o, p, km = nearest_neighbour_route(G, "A", ["B", "D"])
        self.assertEqual(o, ["B", "D"]); self.assertEqual(km, 12)
unittest.main()
