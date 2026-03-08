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
# APPROACH 3: BITMASK
# Time  : O(n * 2^n)
# Space : O(1)  — no recursion stack
#
# Core idea:
#   For n elements, there are exactly 2^n subsets.
#   Every integer from 0 to 2^n-1 has a unique binary pattern of n bits.
#   We use each integer as a "blueprint" — each bit says include or exclude.
#
#   Bit position i is SET   (1) → include nums[i]
#   Bit position i is UNSET (0) → exclude nums[i]
#
# Example: nums = [1, 2, 3],  n = 3  →  2^3 = 8 masks (0 through 7)
#
#   mask  binary   bit2 bit1 bit0   subset
#   ────  ──────   ──── ──── ────   ──────
#     0   000       0    0    0     []            ← no bits set, include nothing
#     1   001       0    0    1     [1]           ← bit 0 set → include nums[0]=1
#     2   010       0    1    0     [2]           ← bit 1 set → include nums[1]=2
#     3   011       0    1    1     [1, 2]        ← bits 0,1 set
#     4   100       1    0    0     [3]           ← bit 2 set → include nums[2]=3
#     5   101       1    0    1     [1, 3]        ← bits 0,2 set
#     6   110       1    1    0     [2, 3]        ← bits 1,2 set
#     7   111       1    1    1     [1, 2, 3]     ← all bits set, include everything
#
# How we CHECK if bit i is set in mask:
#   mask & (1 << i)
#   │         └── creates a number with ONLY bit i set: 1, 2, 4, 8, ...
#   └── AND with mask: result is non-zero only if mask also has bit i set
#
#   e.g. mask=5 (101), i=0: 101 & 001 = 001 ≠ 0 → include nums[0]
#        mask=5 (101), i=1: 101 & 010 = 000 = 0 → skip nums[1]
#        mask=5 (101), i=2: 101 & 100 = 100 ≠ 0 → include nums[2]
#
# How we generate all 2^n masks:
#   range(1 << n)  →  range(2^n)  →  0, 1, 2, ..., 2^n - 1
# ─────────────────────────────────────────────────────────────────────────────
def subsets_bitmask(nums: list) -> list:
    n = len(nums)
    result = []
    for mask in range(1 << n):      # iterate over every possible bitmask (0 to 2^n-1)
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result


# Same logic written explicitly (easier to trace):
def subsets_bitmask_2(nums):
    n = len(nums)
    result = []

    for mask in range(1 << n):      # 2^n masks total
        subset = []

        for i in range(n):          # check each bit position 0..n-1
            if mask & (1 << i):     # is bit i set in this mask?
                subset.append(nums[i])  # yes → include nums[i] in this subset

        result.append(subset)       # this mask's subset is complete

    return result
