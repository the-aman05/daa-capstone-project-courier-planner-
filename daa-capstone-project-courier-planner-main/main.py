"""Intelligent Courier Planning System - integrated pipeline.
Usage: python main.py [--capacity 40]"""
import argparse
from utils import load_parcels
from sorting import merge_sort
from knapsack import knapsack
from graph import load_graph, nearest_neighbour_route

def run(parcels_csv="data/parcels.csv", roads_csv="data/roads.csv", capacity=40, verbose=True):
    parcels = load_parcels(parcels_csv)
    graph = load_graph(roads_csv)

    # Phase 2: sort then knapsack
    ordered = merge_sort(parcels)
    value, chosen, _ = knapsack(ordered, capacity)

    # Phase 3: route over the destinations of chosen parcels
    stops = {p["dest"] for p in chosen}
    order, full_path, km = nearest_neighbour_route(graph, "Depot", stops)

    if verbose:
        print("=== SORTED PARCELS (deadline, then priority) ===")
        for p in ordered:
            print(f"{p['id']}  dest={p['dest']:<9} w={p['weight']:>2}kg  prio={p['priority']:>2}  due={p['deadline']}h")
        print(f"\n=== PACKING PLAN (capacity {capacity} kg) ===")
        for p in chosen:
            print(f"{p['id']} -> {p['dest']}  ({p['weight']} kg, prio {p['priority']})")
        print(f"Total weight: {sum(p['weight'] for p in chosen)} kg | Total priority value: {value}")
        left = [p['id'] for p in ordered if p not in chosen]
        print("Left for next trip:", ", ".join(left) or "none")
        print("\n=== DELIVERY ROUTE ===")
        print("Stop order  :", " -> ".join(["Depot"] + order + ["Depot"]))
        print("Full path   :", " -> ".join(full_path))
        print(f"Route length: {km:.1f} km")
    return chosen, order, full_path, km

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--capacity", type=int, default=40)
    run(capacity=ap.parse_args().capacity)
