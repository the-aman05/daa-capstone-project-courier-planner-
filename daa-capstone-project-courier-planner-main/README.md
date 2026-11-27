# Intelligent Courier Planning System (Capstone)

Python prototype that takes parcels + a road network and produces a **priority-sorted parcel list, an optimal packing plan, and an ordered delivery route**.

## Phase 1 - Problem Design
**Parcel:** `id, dest (graph node), weight (kg), priority (1-10), deadline (hours)`
**Graph:** undirected weighted graph (`data/roads.csv`: from, to, km), node `Depot` is the start/end.
**Vehicle:** capacity in kg (default 40).

| Sub-problem | Algorithm | Why | Complexity |
|---|---|---|---|
| Parcel ordering | Merge Sort (deadline asc, priority desc) | Stable, guaranteed O(n log n) | O(n log n) |
| Which parcels fit in one trip | 0/1 Knapsack DP | Maximises total priority within weight limit; greedy can be suboptimal | O(n·W) |
| Shortest paths between points | Dijkstra (min-heap) | Non-negative km weights | O((V+E) log V) |
| Visiting order of stops | Nearest-Neighbour TSP | Fast approximation; exact TSP is NP-hard | O(k·(V+E) log V) |

**Pipeline:** `load -> merge sort -> knapsack -> destinations of chosen parcels -> NN-TSP using Dijkstra distances -> route + km`

## Run
```
pip install matplotlib      # only needed for benchmark chart
python main.py --capacity 40
python tests.py
python benchmark.py         # writes output/runtime_chart.png
```

## Phase 2 - Sorting & Knapsack (sample result, `output/sample_run.txt`)
Chosen: P03, P02, P01, P05, P08 - 38 kg, priority value 35. Remaining parcels wait for the next trip.

## Phase 3 - Route (sample result)
`Depot -> Market -> Campus -> Library -> Hospital -> Depot`, full path via Mall, **29.0 km**.

## Phase 4 - Performance (`output/benchmark_results.txt`, `output/runtime_chart.png`)
Merge sort vs insertion sort at n=800: ~2 ms vs ~28 ms, confirming O(n log n) vs O(n²).
Knapsack time grows linearly with n for fixed capacity. NN-TSP is the most expensive step because it runs Dijkstra from every stop.

**Future optimisations:** 2-opt improvement on the NN tour; compute Dijkstra once per stop and cache; space-optimised 1-D knapsack table; multi-trip/multi-vehicle assignment; time-window constraints; A* for large road networks.

## Limitations
NN-TSP is not optimal (can be ~25% worse than best tour); knapsack uses integer kg weights; one vehicle and one trip.

## Structure
`main.py` pipeline · `sorting.py` · `knapsack.py` · `graph.py` · `utils.py` · `benchmark.py` · `tests.py` · `data/` · `output/`
