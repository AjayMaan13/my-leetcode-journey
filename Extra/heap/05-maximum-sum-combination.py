"""
Maximum Sum Combination (TUF+)
Difficulty: Medium
Topics: Array, Sorting, Heap (Priority Queue), Greedy

Problem:
    Given two integer arrays nums1 and nums2 and integer k, return the k
    largest possible sums where each sum picks exactly one element from
    each array. Return results in non-increasing order.

Examples:
    nums1=[7,3], nums2=[1,6], k=2       →  [13, 9]
      13 = 7+6,  9 = 3+6

    nums1=[3,4,5], nums2=[2,6,3], k=2  →  [11, 10]
      11 = 5+6,  10 = 4+6

Constraints:
    1 <= nums1.length, nums2.length <= 10^5
    -10^9 <= nums1[i], nums2[i] <= 10^9
    1 <= k <= nums1.length * nums2.length
"""

import heapq


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE — Generate All Pairs
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Generate every possible (nums1[i] + nums2[j]) pair sum.
#   Sort all sums descending. Return first k.
#
# Why it's slow:
#   N * M pairs generated even if k = 1.
#   For N = M = 10^5 that's 10^10 pairs — completely intractable.
#
# Time:  O(N*M + N*M*log(N*M))  →  O(N*M*log(N*M))
# Space: O(N*M)  — stores all pair sums
# ─────────────────────────────────────────────────────────────────────────────

def maxCombinations_brute(nums1, nums2, k):
    all_sums = []

    for a in nums1:
        for b in nums2:
            all_sums.append(a + b)

    all_sums.sort(reverse=True)
    return all_sums[:k]


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: OPTIMAL — Max-Heap + Visited Set (Best-First Search)
# ─────────────────────────────────────────────────────────────────────────────
# Key Insight:
#   After sorting both arrays descending, the globally largest sum is
#   always nums1[0] + nums2[0]. The NEXT largest sum can only come from
#   one of two moves:
#     - Move index i forward in nums1: (i+1, j)
#     - Move index j forward in nums2: (i, j+1)
#
#   This is a best-first search over a 2D grid of pair sums, where
#   both axes are sorted descending. We only ever explore the frontier
#   of potentially largest sums — never all N*M pairs.
#
# Algorithm:
#   1. Sort both arrays descending.
#   2. Push (-(nums1[0]+nums2[0]), 0, 0) into a min-heap (negated = max-heap).
#   3. Mark (0,0) as visited.
#   4. Repeat k times:
#      a. Pop the largest sum (i, j).
#      b. Add to result.
#      c. Push (i+1, j) and (i, j+1) if not yet visited.
#   5. Return result.
#
# Why the visited set?
#   Both (i+1,j) expanding from (i,j) AND (i,j+1) expanding from (i+1,j)
#   could push (i+1,j+1). Without tracking, we'd push duplicates into the
#   heap and return the same sum multiple times.
#
# Visual trace — nums1=[7,3], nums2=[6,1], k=2:
#
#         j=0(6)  j=1(1)
#   i=0(7)  13      8
#   i=1(3)   9      4
#
#   heap: [(-13, 0,0)], visited={(0,0)}
#   pop (-13,0,0) → result=[13]
#     push (i+1,j)=(1,0): -(3+6)=-9  → heap=[(-9,1,0)]
#     push (i,j+1)=(0,1): -(7+1)=-8  → heap=[(-9,1,0),(-8,0,1)]
#   pop (-9,1,0) → result=[13,9]  ← done (k=2)
#
# Time:  O(N log N + M log M + k log k)
#          sort      sort      k heap ops, heap size ≤ 2k
# Space: O(k)  — heap + visited set, both bounded by 2k entries
# ─────────────────────────────────────────────────────────────────────────────

def maxCombinations_optimal(nums1, nums2, k):
    # Sort both descending so largest elements come first
    nums1.sort(reverse=True)
    nums2.sort(reverse=True)

    # Max-heap via negation: stores (-sum, i, j)
    max_heap = [(-(nums1[0] + nums2[0]), 0, 0)]

    # Visited set to prevent duplicate (i,j) pairs in the heap
    visited = {(0, 0)}

    result = []

    for _ in range(k):
        neg_sum, i, j = heapq.heappop(max_heap)
        result.append(-neg_sum)

        # Explore neighbour: advance i (next element in nums1)
        if i + 1 < len(nums1) and (i + 1, j) not in visited:
            heapq.heappush(max_heap, (-(nums1[i + 1] + nums2[j]), i + 1, j))
            visited.add((i + 1, j))

        # Explore neighbour: advance j (next element in nums2)
        if j + 1 < len(nums2) and (i, j + 1) not in visited:
            heapq.heappush(max_heap, (-(nums1[i] + nums2[j + 1]), i, j + 1))
            visited.add((i, j + 1))

    return result


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    test_cases = [
        # (nums1, nums2, k, expected)
        ([7, 3],      [1, 6],    2, [13, 9]),
        ([3, 4, 5],   [2, 6, 3], 2, [11, 10]),
        ([1, 2],      [3, 4],    1, [6]),           # only want top 1: 2+4=6
        ([1, 2],      [3, 4],    4, [6, 5, 5, 4]),  # all pairs: 6,5,5,4
        ([1],         [1],       1, [2]),            # single elements
        ([0, 0],      [0, 0],    2, [0, 0]),         # all zeros
        ([-1, -2],    [-3, -4],  2, [-4, -5]),       # negatives
        ([5, 5],      [5, 5],    3, [10, 10, 10]),   # duplicates
    ]

    approaches = [
        ("Brute Force",  maxCombinations_brute),
        ("Optimal Heap", maxCombinations_optimal),
    ]

    all_passed = True
    for nums1, nums2, k, expected in test_cases:
        for name, fn in approaches:
            result = fn(nums1[:], nums2[:], k)
            if result != expected:
                all_passed = False
                print(f"  ✗ FAIL | {name} | nums1={nums1}, nums2={nums2}, k={k} | got {result}, expected {expected}")

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
# Approach          Time                        Space     Notes
# ──────────────────────────────────────────────────────────────────────────────
# Brute Force       O(N*M*log(N*M))             O(N*M)    Generates all pairs
# Optimal Heap      O(N logN + M logM + k logk) O(k)      Best-first search
#
# ─────────────────────────────────────────────────────────────────────────────
# PATTERN NOTE
# ─────────────────────────────────────────────────────────────────────────────
# This is the same 2D grid best-first search pattern as:
#   - LC 373: Find K Pairs with Smallest Sums (identical structure, min instead)
#   - LC 378: Kth Smallest Element in a Sorted Matrix
#
# ─────────────────────────────────────────────────────────────────────────────
# README — Heap Section Update
# ─────────────────────────────────────────────────────────────────────────────
#
# | # | Problem | Difficulty | Approach |
# |---|---------|------------|----------|
# | - | Maximum Sum Combination | Medium | Sort desc + max-heap best-first search;
# |   |                         |        | visited set prevents duplicates;
# |   |                         |        | same pattern as LC 373 / LC 378 |