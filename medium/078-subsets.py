"""
LeetCode 78. Subsets  |  Medium

Problem Statement:
    Given an integer array nums of UNIQUE elements, return ALL possible
    subsets (the power set). Result must not contain duplicate subsets.

Examples:
    nums = [1,2,3]  →  [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
    nums = [0]      →  [[],[0]]

Key Insight:
    For n unique elements, there are exactly 2^n subsets.
    At each element we make a binary decision: INCLUDE or EXCLUDE.
    This is the exact same power-set recursion from "Power Set / Subsequences
    of a String" — applied to an integer array.

    Recursion tree for [1,2,3]:
                        solve(0, [])
                    /               \\
          solve(1,[1])           solve(1,[])
          /        \\             /         \\
    solve(2,[1,2]) solve(2,[1]) solve(2,[2]) solve(2,[])
      /   \\         /   \\       /   \\        /   \\
  [1,2,3][1,2]  [1,3][1]   [2,3][2]   [3]  []
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: YOUR V1 — Binary Include/Exclude (decision-tree style)
# Time  : O(n * 2^n)  — 2^n subsets, each up to length n to copy
# Space : O(n)        — recursion depth = n
#
# At each index, make exactly 2 choices:
#   1. INCLUDE nums[index], recurse to index+1
#   2. EXCLUDE nums[index], recurse to index+1
#
# Only adds to result at the BASE CASE (index == len(nums)).
# Every path from root to leaf is one complete subset.
#
# One note: result.sort() at the end is optional — the problem says
# "any order", but it's fine to sort for consistent output.
# ─────────────────────────────────────────────────────────────────────────────
def subsets_v1(nums: list) -> list:
    if not nums:
        return [[]]   # edge case: empty array has one subset — the empty set

    def solve(index: int, currList: list, result: list) -> None:
        # Base case: all elements considered → this path is a complete subset
        if index == len(nums):
            result.append(currList[:])  # snapshot the current state
            return

        # Choice 1: INCLUDE nums[index]
        currList.append(nums[index])
        solve(index + 1, currList, result)
        currList.pop()   # backtrack — undo the include

        # Choice 2: EXCLUDE nums[index]
        solve(index + 1, currList, result)

    result = []
    solve(0, [], result)
    result.sort()   # optional — for lexicographic ordering
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR V2 — Loop-based (add-before-recurse style)  ← preferred
# Time  : O(n * 2^n)
# Space : O(n)
#
# Instead of waiting until the base case, add the CURRENT subset to result
# immediately at the START of every recursive call.
#
# Then loop from `index` to end, picking each element as the "next" element
# to add. This naturally generates all subsets without duplicates because
# we always pick elements at positions GREATER THAN the current index
# (the `range(index, len(nums))` loop).
#
# How it builds subsets for [1,2,3]:
#
#   solve(0,[])        → add []
#     pick 1 → solve(1,[1])     → add [1]
#       pick 2 → solve(2,[1,2]) → add [1,2]
#         pick 3 → solve(3,[1,2,3]) → add [1,2,3]
#       pick 3 → solve(3,[1,3]) → add [1,3]
#     pick 2 → solve(2,[2])     → add [2]
#       pick 3 → solve(3,[2,3]) → add [2,3]
#     pick 3 → solve(3,[3])     → add [3]
#
#   All 8 subsets generated: [], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]
#
# ── WHY THIS WORKS WITHOUT DUPLICATES ───────────────────────────────────────
# The loop starts at `index` (not 0).
# Each recursive call starts its loop from i+1 (not from i or 0).
# This ensures:
#   - We never re-pick an element we've already passed
#   - Every subset is generated in increasing index order
#   - No two paths generate the same combination
#
# Compare to Combination Sum problems:
#   Combination Sum  I  (unlimited reuse): solve(i,   ...)  ← same i
#   Combination Sum  II (use once each):   solve(i+1, ...)  ← next i
#   Subsets              (use once each):   solve(i+1, ...)  ← same structure
#
# ── WHY V2 IS CLEANER THAN V1 ────────────────────────────────────────────────
# V1 always goes to depth n before adding anything → every path is length n
# V2 adds the current state IMMEDIATELY at every level → naturally captures
#    subsets of all lengths (0 through n) without needing a base case check
# ─────────────────────────────────────────────────────────────────────────────
def subsets_v2(nums: list) -> list:
    if not nums:
        return [[]]

    def solve(index: int, currList: list, result: list) -> None:
        # Add the current subset IMMEDIATELY (captures all lengths 0..n)
        result.append(currList[:])

        # Try adding each remaining element as the next element of the subset
        for i in range(index, len(nums)):
            currList.append(nums[i])        # choose nums[i]
            solve(i + 1, currList, result)  # recurse — next pick must come after i
            currList.pop()                  # backtrack

    result = []
    solve(0, [], result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: BITMASK (from Power Set / Subsequences problem)
# Time  : O(n * 2^n)
# Space : O(1)  — no recursion stack
#
# Every number 0 to 2^n-1 represents a subset via its binary bits.
# Bit i set → include nums[i].
# Included here to show the connection to the "Power Set of a String" problem.
# ─────────────────────────────────────────────────────────────────────────────
def subsets_bitmask(nums: list) -> list:
    n = len(nums)
    result = []
    for mask in range(1 << n):      # 0 to 2^n - 1
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result

