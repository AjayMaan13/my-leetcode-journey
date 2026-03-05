"""
PROBLEM: M-Coloring Problem
=============================

Given an undirected graph and a number m, determine if the graph can be
colored with at most m colors such that no two adjacent vertices share
the same color.

Examples:
    N=4, M=3, Edges=[(0,1),(1,2),(2,3),(3,0),(0,2)] → 1 (possible)
    N=3, M=2, Edges=[(0,1),(1,2),(0,2)]             → 0 (triangle needs 3 colors)

Output: 1 if colorable, 0 if not.

Key insight: process nodes one by one (0 → n-1). For each node, try every
color. If a color doesn't clash with any already-colored neighbor, assign it
and recurse to the next node. If no color works, backtrack.
"""


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 1: Your original attempt — graph-traversal style (buggy)
# ─────────────────────────────────────────────────────────────────────────────
# Issue: traverses via graph edges (neighbour-to-neighbour) instead of
# iterating nodes 0..n-1 in order. This means:
#   1. Isolated nodes are never visited.
#   2. The same node can be visited via multiple neighbours, causing
#      duplicate work and wrong backtracking.
#   3. The `complete()` check is O(n) on every recursive call.
# Included here only for reference / learning — see v2 for the fix.

def graphColoring_v1_buggy(edges, m):
    n                = max(max(u, v) for u, v in edges) + 1
    colors_assigned  = {i: -1 for i in range(n)}
    graph            = {i: [] for i in range(n)}
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    colors = list(range(m))

    def complete(colors_assigned):
        return all(c != -1 for c in colors_assigned.values())

    def safeColors(node, color):
        return all(color != colors_assigned[nb] for nb in graph[node])

    def backtrack(node):
        if complete(colors_assigned):
            return True
        # BUG: iterates neighbours of `node`, not ALL uncoloured nodes
        for nb in graph[node]:
            if colors_assigned[nb] != -1:
                continue
            for color in colors:
                if safeColors(nb, color):
                    colors_assigned[nb] = color
                    if backtrack(nb):
                        return True
                    colors_assigned[nb] = -1
        return False

    colors_assigned[0] = 0
    return backtrack(0)


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 2: Your fixed version — node-by-node backtracking  ✓
# ─────────────────────────────────────────────────────────────────────────────
# Process nodes in order 0, 1, 2, ..., n-1.
# For each node, try colors 0..m-1. Assign the first safe color and recurse
# to the NEXT node (node+1). If no color works → backtrack.
# Base case: node == n → all nodes colored → return True.
#
# This avoids all the bugs in v1:
#   - Every node is visited exactly once.
#   - No O(n) `complete()` check needed — the index IS the progress tracker.
#
# Time:  O(m^n)  — m choices at each of n nodes (worst case)
# Space: O(n)    — recursion depth + colors_assigned dict

def graphColoring_v2(edges, m):
    n               = max(max(u, v) for u, v in edges) + 1
    colors_assigned = [-1] * n          # use list for O(1) index access
    graph           = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def isSafe(node, color):
        """True if no neighbour of `node` already has `color`."""
        return all(colors_assigned[nb] != color for nb in graph[node])

    def backtrack(node):
        if node == n:                   # all nodes successfully colored
            return True

        for color in range(m):
            if isSafe(node, color):
                colors_assigned[node] = color
                if backtrack(node + 1):
                    return True
                colors_assigned[node] = -1   # backtrack

        return False                    # no color worked for this node

    return 1 if backtrack(0) else 0


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 3: Cleaner rewrite — same logic, more readable  ← recommended
# ─────────────────────────────────────────────────────────────────────────────
# Identical algorithm to v2, but:
#   - Builds adjacency set (faster O(1) neighbor lookup)
#   - Separates graph building from solving cleanly
#   - Uses a color array indexed by node for clarity

def graphColoring(edges, m, n=None):
    """
    edges : list of (u, v) pairs
    m     : number of colors available
    n     : number of nodes (auto-detected from edges if not given)
    """
    if not edges:
        return 1    # no edges → any single color works

    if n is None:
        n = max(max(u, v) for u, v in edges) + 1

    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * n    # color[i] = color assigned to node i, -1 = uncolored

    def isSafe(node, c):
        """Check if color c can be assigned to node without conflict."""
        for neighbor in adj[node]:
            if color[neighbor] == c:
                return False
        return True

    def solve(node):
        """Try to color nodes node, node+1, ..., n-1."""
        if node == n:           # all nodes colored → found a valid coloring
            return True

        for c in range(m):      # try each color
            if isSafe(node, c):
                color[node] = c
                if solve(node + 1):
                    return True
                color[node] = -1    # backtrack

        return False            # no valid color found for this node

    return 1 if solve(0) else 0


# ─────────────────────────────────────────────────────────────────────────────
# Step-by-step trace for Example 1 (N=4, M=3)
# ─────────────────────────────────────────────────────────────────────────────
#
# Graph:  0─1, 1─2, 2─3, 3─0, 0─2   (0 connects to 1, 2, 3)
#
# solve(0): try color 0 → safe → color=[0,-1,-1,-1]
#   solve(1): try color 0 → neighbor 0 has 0 ✗
#             try color 1 → safe → color=[0,1,-1,-1]
#     solve(2): try color 0 → neighbor 1 has 1 (ok), neighbor 0 has 0 ✗
#               try color 1 → neighbor 1 has 1 ✗
#               try color 2 → safe → color=[0,1,2,-1]
#       solve(3): try color 0 → neighbor 2 has 2 (ok), neighbor 0 has 0 ✗
#                 try color 1 → safe → color=[0,1,2,1]
#         solve(4): node==n → return True ✅


# ─────────────────────────────────────────────────────────────────────────────
# Complexity
# ─────────────────────────────────────────────────────────────────────────────
#
#  Worst case: O(m^n) time — at each of n nodes we try up to m colors
#  Space:      O(n)        — color array + recursion stack depth n
#
#  In practice much faster due to pruning: isSafe() cuts branches early.
