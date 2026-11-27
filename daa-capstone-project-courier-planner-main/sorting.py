"""Phase 2a - Parcel sorting. Merge sort (O(n log n)) vs insertion sort (O(n^2)) for comparison."""

def key(p):
    # earlier deadline first; ties broken by higher priority
    return (p["deadline"], -p["priority"])

def merge_sort(items, k=key):
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    l, r = merge_sort(items[:mid], k), merge_sort(items[mid:], k)
    out, i, j = [], 0, 0
    while i < len(l) and j < len(r):
        if k(l[i]) <= k(r[j]):
            out.append(l[i]); i += 1
        else:
            out.append(r[j]); j += 1
    return out + l[i:] + r[j:]

def insertion_sort(items, k=key):
    a = items[:]
    for i in range(1, len(a)):
        cur, j = a[i], i - 1
        while j >= 0 and k(a[j]) > k(cur):
            a[j + 1] = a[j]; j -= 1
        a[j + 1] = cur
    return a
