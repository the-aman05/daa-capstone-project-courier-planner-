import csv, random

def load_parcels(path):
    with open(path) as f:
        return [{"id": r["id"], "dest": r["dest"], "weight": int(r["weight"]),
                 "priority": int(r["priority"]), "deadline": int(r["deadline"])}
                for r in csv.DictReader(f)]

def generate_parcels(n, nodes, seed=1):
    rnd = random.Random(seed)
    return [{"id": f"P{i:04d}", "dest": rnd.choice(nodes), "weight": rnd.randint(1, 15),
             "priority": rnd.randint(1, 10), "deadline": rnd.randint(1, 48)} for i in range(n)]

def generate_graph(n, seed=1):
    """Connected random graph: chain backbone + extra random edges. Node 0 = Depot."""
    rnd = random.Random(seed)
    names = ["Depot"] + [f"C{i}" for i in range(1, n)]
    g = {x: {} for x in names}
    def add(a, b):
        d = round(rnd.uniform(1, 20), 1); g[a][b] = d; g[b][a] = d
    for i in range(1, n): add(names[i - 1], names[i])
    for _ in range(n * 2):
        a, b = rnd.sample(names, 2)
        if b not in g[a]: add(a, b)
    return g
