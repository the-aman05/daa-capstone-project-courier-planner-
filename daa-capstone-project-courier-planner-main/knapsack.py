"""Phase 2b - 0/1 Knapsack (Dynamic Programming) to choose parcels for one trip."""

def knapsack(parcels, capacity):
    """Returns (best_value, chosen_parcels, dp_table). Weights are ints (kg)."""
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, p in enumerate(parcels, 1):
        w, v = p["weight"], p["priority"]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c and dp[i - 1][c - w] + v > dp[i][c]:
                dp[i][c] = dp[i - 1][c - w] + v
    chosen, c = [], capacity
    for i in range(n, 0, -1):          # backtrack
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(parcels[i - 1]); c -= parcels[i - 1]["weight"]
    return dp[n][capacity], chosen[::-1], dp
