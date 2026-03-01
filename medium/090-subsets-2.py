"""
LeetCode 90. Subsets II  |  Medium

Problem Statement:
    Given an integer array nums that MAY CONTAIN DUPLICATES, return all
    possible subsets (the power set). Result must NOT contain duplicate subsets.

Examples:
    nums = [1,2,2]  →  [[], [1], [1,2], [1,2,2], [2], [2,2]]
    nums = [0]      →  [[], [0]]

How this fits into the progression:
    ┌─────────────────┬──────────────┬──────────────┬──────────────────────┐
    │ Problem         │ Duplicates   │ Reuse        │ Dedup strategy       │
    ├─────────────────┼──────────────┼──────────────┼──────────────────────┤
    │ Subsets (78)    │ No           │ No           │ None needed          │
    │ Comb. Sum I     │ No           │ Yes          │ None needed          │
    │ Comb. Sum II    │ Yes          │ No           │ i>index + same value │
    │ Subsets II (90) │ Yes          │ No           │ i>index + same value │
    └─────────────────┴──────────────┴──────────────┴──────────────────────┘

    Subsets II = Subsets (78) + the SAME duplicate-skip from Combination Sum II.
    Your solution is already correct and optimal.
"""


# ─────────────────────────────────────────────────────────────────────────────
# YOUR SOLUTION  (optimal — fully commented)
# Time  : O(n * 2^n)  — at most 2^n subsets, each up to length n to copy
# Space : O(n)        — recursion depth = n
#
# This is literally Subsets (78) V2 (loop + add-first) with ONE extra line:
#   `if i > index and nums[i] == nums[i-1]: continue`
#
# ── WHY THE SKIP WORKS ───────────────────────────────────────────────────────
# After sorting, duplicates are adjacent: [1, 2, 2] → dupes sit next to each other.
#
# The loop at each recursion level decides "which element to pick NEXT."
# If we pick nums[i], we explore ALL subsets that contain that value at
# this position. If the NEXT element nums[i+1] has the same value, picking
# it would produce the EXACT SAME set of subsets again → skip it.
#
# Condition: `i > index AND nums[i] == nums[i-1]`
#   i > index    → not the first pick of this loop level (first is always allowed)
#   nums[i]==... → same value as the one we JUST explored at this level
#
# Example: nums=[1,2,2], sorted → [1,2,2]
#
#   solve(0, []):
#     add []
#     i=0: pick 1 → solve(1, [1])
#       add [1]
#       i=1: pick 2 → solve(2, [1,2])
#         add [1,2]
#         i=2: pick 2 → solve(3, [1,2,2])
#           add [1,2,2]  ✓
#       i=2: i>index(1) AND nums[2]==nums[1] (2==2) → SKIP  ← prevents [1,2] again
#     i=1: pick 2 → solve(2, [2])
#       add [2]
#       i=2: pick 2 → solve(3, [2,2])
#         add [2,2]  ✓
#     i=2: i>index(0) AND nums[2]==nums[1] (2==2) → SKIP  ← prevents [2] duplicate
#
#   Final result: [], [1], [1,2], [1,2,2], [2], [2,2]  ✓  (6 unique subsets)
#
# WITHOUT the skip (using raw Subsets 78 logic on [1,2,2]):
#   Would generate: [], [1], [1,2], [1,2,2], [1,2], [1,2,2], [2], [2,2], [2], [2,2]
#                                   ^ dupe       ^ dupe          ^ dupe   ^ dupe
#
# ── WHY i > index NOT i > 0 ─────────────────────────────────────────────────
# Same reason as Combination Sum II — if we used `i > 0`, we'd accidentally
# skip valid subsets that NEED the second occurrence of a value.
#
# Example: nums=[2,2], target=any. After picking nums[0]=2 at the outer level,
# we call solve(index=1, [2], ...). Inside, i=1 is the FIRST pick of this
# level (i == index == 1). If we used `i > 0`, i=1 > 0 is True and
# nums[1]==nums[0] would skip it → we'd never generate [2,2] ← WRONG.
#
# `i > index` prevents this: at index=1, i=1 → `1 > 1` is False → allowed ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def subsetsWithDup(self, nums: list) -> list:
        if not nums:
            return [[]]   # empty array → one subset: the empty set

        nums.sort()   # REQUIRED: groups duplicates together so the skip works

        def solve(index: int, curr: list, result: list) -> None:
            # Add current subset IMMEDIATELY (captures subsets of all sizes)
            result.append(curr[:])

            for i in range(index, len(nums)):
                # ── DUPLICATE SKIP ────────────────────────────────────────────
                # If this is NOT the first element of the loop at this level (i>index)
                # AND it has the same value as the previous element (nums[i]==nums[i-1])
                # → we already generated all subsets using this value at this position
                # → skip to avoid duplicate subsets in the result
                if i > index and nums[i] == nums[i - 1]:
                    continue

                curr.append(nums[i])         # choose nums[i]
                solve(i + 1, curr, result)   # recurse — next pick must come after i (no reuse)
                curr.pop()                   # backtrack — undo the choice

        result = []
        solve(0, [], result)
        return result
