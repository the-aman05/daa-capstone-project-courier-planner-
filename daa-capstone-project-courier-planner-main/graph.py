"""Phase 3 - Customer graph, Dijkstra shortest paths, nearest-neighbour TSP approximation."""
import csv, heapq

def load_graph(path):
    g = {}
    with open(path) as f:
        for r in csv.DictReader(f):
            a, b, d = r["from"], r["to"], float(r["km"])
            g.setdefault(a, {})[b] = d
            g.setdefault(b, {})[a] = d     # undirected roads
    return g

def dijkstra(g, src):
    dist = {n: float("inf") for n in g}; prev = {}
    dist[src] = 0; pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in g[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd; prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def path_to(prev, src, dst):
    p = [dst]
    while p[-1] != src:
        p.append(prev[p[-1]])
    return p[::-1]

def nearest_neighbour_route(g, depot, stops):
    """Greedy TSP approximation. Returns (ordered stops, full node path, total km)."""
    stops = set(stops) - {depot}
    cur, order, full, total = depot, [], [depot], 0.0
    while stops:
        dist, prev = dijkstra(g, cur)
        nxt = min(stops, key=lambda s: dist[s])
        seg = path_to(prev, cur, nxt)
        full += seg[1:]; total += dist[nxt]
        order.append(nxt); stops.remove(nxt); cur = nxt
    dist, prev = dijkstra(g, cur)          # return to depot
    full += path_to(prev, cur, depot)[1:]; total += dist[depot]
    return order, full, total
