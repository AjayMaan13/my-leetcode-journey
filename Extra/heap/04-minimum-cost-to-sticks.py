"""
Minimum Cost to Connect Sticks
https://algo.monster/problems/connect_sticks (TUF+ / Amazon OA classic)
Difficulty: Medium
Topics: Greedy, Heap (Priority Queue)

Problem:
    Given sticks with positive integer lengths, connect any two sticks into one
    by paying cost = sum of their lengths. Repeat until one stick remains.
    Return the minimum total cost.

Examples:
    sticks = [2, 4, 3]      →  14
      connect 2+3=5 (cost 5), connect 4+5=9 (cost 9)  →  5+9=14

    sticks = [1, 8, 3, 5]   →  30
      connect 1+3=4 (cost 4), connect 4+5=9 (cost 9), connect 8+9=17 (cost 17)
      →  4+9+17=30

Constraints:
    1 <= sticks.length <= 10^4
    1 <= sticks[i] <= 10^4

Key Insight (why always merge the two smallest?):
    Every time two sticks are merged, the resulting stick gets added to future
    merges. Merging LARGER sticks early means they get counted in more future
    costs. Merging the two SMALLEST sticks first minimises the compounding.
    This is the same greedy as Huffman Encoding.
"""

import heapq
import math
from itertools import combinations


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE — Try All Merge Orders
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   At each step, try every possible pair of sticks to merge.
#   Recurse on the resulting array and track the minimum total cost.
#   Explores ALL merge orderings → guaranteed optimal but exponential.
#
# Why it's slow:
#   At each step with k sticks, there are C(k,2) = k*(k-1)/2 pair choices.
#   Total states: N! / 2^(N-1) orderings — factorial explosion.
#   For N=10 already ~100k calls; N=20 is intractable.
#
# Time:  O(N! * N)  — factorial merge orderings × cost of each step
# Space: O(N^2)     — recursion depth * list copies
# ─────────────────────────────────────────────────────────────────────────────

def connectSticks_brute(sticks):
    if len(sticks) == 1:
        return 0

    min_cost = math.inf

    # Try every pair (i, j) as the next merge
    for i in range(len(sticks)):
        for j in range(i + 1, len(sticks)):
            merged = sticks[i] + sticks[j]
            cost = merged

            # Build remaining sticks after merging i and j
            remaining = [sticks[k] for k in range(len(sticks)) if k != i and k != j]
            remaining.append(merged)

            total = cost + connectSticks_brute(remaining)
            min_cost = min(min_cost, total)

    return min_cost


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: GREEDY — Sort + Simulate (Suboptimal Implementation)
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   The greedy insight: always merge the two smallest sticks.
#   Simulate with a sorted list — after each merge, insert the new stick
#   back in sorted position and repeat.
#
# Why this is correct:
#   Merging small sticks first means the larger merged result participates
#   in fewer future merges, minimising total compounding cost.
#   (Same principle as Huffman coding — optimal prefix-free codes.)
#
# Why this is still slow:
#   Re-sorting after every merge is O(N log N) per step → O(N^2 log N) total.
#   Insertion into a sorted list is O(N) due to shifting.
#
# Time:  O(N^2 log N)  — N merges, each re-sorts O(N log N)
# Space: O(N)
# ─────────────────────────────────────────────────────────────────────────────

def connectSticks_greedy_sort(sticks):
    if len(sticks) == 1:
        return 0

    sticks = sorted(sticks)   # start sorted
    total_cost = 0

    while len(sticks) > 1:
        # Two smallest are always at the front (list is maintained sorted)
        a = sticks.pop(0)     # O(N) shift — expensive
        b = sticks.pop(0)     # O(N) shift

        merged = a + b
        total_cost += merged

        # Insert merged back in sorted position: O(N) scan + O(N) shift
        inserted = False
        for i in range(len(sticks)):
            if merged <= sticks[i]:
                sticks.insert(i, merged)
                inserted = True
                break
        if not inserted:
            sticks.append(merged)

    return total_cost


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: OPTIMAL — Min-Heap (Priority Queue)
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Same greedy — always merge the two smallest — but use a min-heap to get
#   and re-insert the minimum in O(log N) instead of O(N).
#
# Algorithm:
#   1. Heapify the sticks array → O(N)
#   2. While more than one stick remains:
#      a. Pop the two smallest  → O(log N) each
#      b. Merge them, add cost
#      c. Push merged back      → O(log N)
#   3. Return total cost.
#
# Visual trace for [2, 4, 3]:
#   heap: [2, 3, 4]
#   pop 2, pop 3 → merged=5, cost=5,  heap: [4, 5]
#   pop 4, pop 5 → merged=9, cost=9,  heap: [9]
#   total = 14 ✓
#
# Visual trace for [1, 8, 3, 5]:
#   heap: [1, 3, 5, 8]
#   pop 1, pop 3 → merged=4,  cost=4,   heap: [4, 5, 8]
#   pop 4, pop 5 → merged=9,  cost=9,   heap: [8, 9]
#   pop 8, pop 9 → merged=17, cost=17,  heap: [17]
#   total = 30 ✓
#
# Time:  O(N log N)  — N-1 merges, each O(log N) heap ops
# Space: O(N)        — in-place heap on input
# ─────────────────────────────────────────────────────────────────────────────

def connectSticks_optimal(sticks):
    if len(sticks) == 1:
        return 0

    heapq.heapify(sticks)          # build min-heap in O(N)
    total_cost = 0

    while len(sticks) > 1:
        a = heapq.heappop(sticks)  # smallest  O(log N)
        b = heapq.heappop(sticks)  # 2nd smallest O(log N)

        merged = a + b
        total_cost += merged

        heapq.heappush(sticks, merged)   # push merged back O(log N)

    return total_cost


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    test_cases = [
        ([2, 4, 3],       14),
        ([1, 8, 3, 5],    30),
        ([5],              0),   # single stick — no merge needed
        ([1, 2],           3),   # one merge
        ([1, 1, 1, 1],    8),   # 1+1=2(2), 1+1=2(2), 2+2=4(4) → 8
        ([3, 3, 3, 3],   24),   # 3+3=6(6), 3+3=6(6), 6+6=12(12) → 24
        ([10, 20, 30],   90),   # 10+20=30(30), 30+30=60(60) → 90
        ([1, 2, 3, 4, 5], 33),  # 1+2=3(3),3+3=6(6),4+5=9(9),6+9=15(15) → 33
    ]

    approaches = [
        ("Brute Force",        connectSticks_brute),
        ("Greedy Sort",        connectSticks_greedy_sort),
        ("Optimal Min-Heap",   connectSticks_optimal),
    ]

    all_passed = True
    for sticks, expected in test_cases:
        for name, fn in approaches:
            # brute force too slow for large inputs — skip those
            if name == "Brute Force" and len(sticks) > 8:
                continue
            result = fn(sticks[:])   # pass copy — heap modifies in place
            status = "✓" if result == expected else "✗"
            if result != expected:
                all_passed = False
                print(f"  {status} FAIL | {name} | sticks={sticks} | got {result}, expected {expected}")

    if all_passed:
        print("All tests passed ✓")
    else:
        print("\nSome tests FAILED — see above.")


if __name__ == "__main__":
    run_tests()


# ─────────────────────────────────────────────────────────────────────────────
# COMPLEXITY SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
#
# Approach              Time            Space   Notes
# ──────────────────────────────────────────────────────────────────────────────
# Brute Force           O(N! · N)       O(N²)   Tries all merge orderings
# Greedy (Sort+List)    O(N² log N)     O(N)    Correct greedy, slow re-sort
# Optimal (Min-Heap)    O(N log N)      O(N)    Same greedy, O(log N) per merge
#
# ─────────────────────────────────────────────────────────────────────────────
# WHY GREEDY IS CORRECT — Intuition
# ─────────────────────────────────────────────────────────────────────────────
#
# Each merge adds the merged value to the heap, so it will be counted again
# in future merges. The longer a stick "lives" in the pool before the final
# merge, the more times its length is added to the total cost.
#
# By always merging the two SMALLEST sticks, we ensure large values are
# created as late as possible — minimising how many times they compound.
#
# This is identical to Huffman Encoding: build the optimal prefix tree by
# always combining the two lowest-frequency nodes.
#
# ─────────────────────────────────────────────────────────────────────────────
# README — Heap Section Update
# ─────────────────────────────────────────────────────────────────────────────
#
# | # | Problem | Difficulty | Approach |
# |---|---------|------------|----------|
# | - | Minimum Cost to Connect Sticks | Medium | Greedy: always merge 2 smallest;
# |   |                                |        | min-heap for O(log N) per merge;
# |   |                                |        | same pattern as Huffman Encoding |