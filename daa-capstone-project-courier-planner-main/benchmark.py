"""Phase 4 - runtime testing on small & larger datasets, produces output/runtime_chart.png"""
import time
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils import generate_parcels, generate_graph
from sorting import merge_sort, insertion_sort
from knapsack import knapsack
from graph import dijkstra, nearest_neighbour_route

def t(fn, *a):
    s = time.perf_counter(); fn(*a); return (time.perf_counter() - s) * 1000

sizes = [50, 100, 200, 400, 800]
rows = {"Merge sort": [], "Insertion sort": [], "Knapsack DP": [], "Dijkstra": [], "NN-TSP route": []}
print(f"{'n':>5} | " + " | ".join(f"{k:>14}" for k in rows) + "   (ms)")
for n in sizes:
    g = generate_graph(n); nodes = list(g)
    ps = generate_parcels(n, nodes)
    stops = nodes[1:min(len(nodes), 25)]
    vals = [t(merge_sort, ps), t(insertion_sort, ps), t(knapsack, ps[:n], 100),
            t(dijkstra, g, "Depot"), t(nearest_neighbour_route, g, "Depot", stops)]
    for k, v in zip(rows, vals): rows[k].append(v)
    print(f"{n:>5} | " + " | ".join(f"{v:>14.2f}" for v in vals))

plt.figure(figsize=(8, 5))
for k, v in rows.items(): plt.plot(sizes, v, marker="o", label=k)
plt.xlabel("Input size (parcels / nodes)"); plt.ylabel("Runtime (ms)")
plt.title("Runtime of major steps"); plt.yscale("log"); plt.grid(alpha=.3); plt.legend()
plt.tight_layout(); plt.savefig("output/runtime_chart.png", dpi=150)
print("Saved output/runtime_chart.png")
