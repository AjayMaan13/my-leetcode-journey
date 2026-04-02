"""
1296. Divide Array in Sets of K Consecutive Numbers
https://leetcode.com/problems/divide-array-in-sets-of-k-consecutive-numbers/
Difficulty: Medium
Topics: Array, Hash Table, Greedy, Sorting

Problem:
    Given an array of integers `nums` and a positive integer `k`, check whether
    it is possible to divide the array into sets of `k` consecutive numbers.

    NOTE: This is identical to LC 846 (Hand of Straights) with groupSize → k.

Examples:
    nums = [1,2,3,3,4,4,5,6],          k = 4  →  True   ([1,2,3,4],[3,4,5,6])
    nums = [3,2,1,2,3,4,3,4,5,9,10,11],k = 3  →  True   ([1,2,3],[2,3,4],[3,4,5],[9,10,11])
    nums = [1,2,3,4],                  k = 3  →  False  (4 % 3 ≠ 0)

Constraints:
    1 <= k <= nums.length <= 10^5
    1 <= nums[i] <= 10^9
"""

import heapq
from collections import Counter


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE — Sort + Counter
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Sort the array. Greedily start a new group from the smallest remaining
#   card. For each group, consume k consecutive values from the Counter.
#   If any consecutive value is missing, return False.
#
# Time:  O(N log N)  — sort dominates
# Space: O(N)        — counter
# ─────────────────────────────────────────────────────────────────────────────

def canDivideIntoSets_brute(nums, k):
    if len(nums) % k != 0:
        return False

    nums_sorted = sorted(nums)
    count = Counter(nums_sorted)

    for num in nums_sorted:
        if count[num] == 0:        # already consumed
            continue
        for i in range(k):
            if count[num + i] == 0:
                return False
            count[num + i] -= 1

    return True


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: OPTIMAL — Min-Heap + Counter
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Use a Counter for frequencies and a min-heap of unique values to always
#   find the current smallest number in O(log N).
#
#   The smallest remaining number can ONLY be the start of a group —
#   there's no smaller number left to pair it with. If we can't complete
#   k consecutive numbers starting from it, return False.
#
# Time:  O(N log N)  — heap ops over unique values
# Space: O(N)        — counter + heap
# ─────────────────────────────────────────────────────────────────────────────

def canDivideIntoSets_heap(nums, k):
    if len(nums) % k != 0:
        return False

    count = Counter(nums)
    min_heap = list(count.keys())
    heapq.heapify(min_heap)

    while min_heap:
        start = min_heap[0]               # peek — smallest remaining value

        if count[start] == 0:             # fully consumed, discard
            heapq.heappop(min_heap)
            continue

        for i in range(k):                # try to form group [start, start+k-1]
            if count[start + i] == 0:
                return False
            count[start + i] -= 1

    return True


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: CLEANEST OPTIMAL — Sorted Keys + Counter
# ─────────────────────────────────────────────────────────────────────────────
# Same greedy logic without a heap — iterate sorted unique keys directly.
# At each key, consume `freq` copies of k consecutive values all at once
# (since that key must start exactly `freq` groups).
#
# Time:  O(N log N)  — sorting unique keys
# Space: O(N)        — counter
# ─────────────────────────────────────────────────────────────────────────────

def canDivideIntoSets_sorted(nums, k):
    if len(nums) % k != 0:
        return False

    count = Counter(nums)

    for num in sorted(count):
        freq = count[num]
        if freq == 0:
            continue
        for i in range(k):               # consume `freq` copies of each of k values
            count[num + i] -= freq
            if count[num + i] < 0:
                return False

    return True


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    test_cases = [
        # (nums, k, expected)
        ([1,2,3,3,4,4,5,6],             4, True),
        ([3,2,1,2,3,4,3,4,5,9,10,11],   3, True),
        ([1,2,3,4],                      3, False),
        ([1,2,3],                        3, True),
        ([1,1,2,2,3,3],                  3, True),
        ([1,2,3,4,5,6],                  3, True),
        ([1,2,3,4,5,6],                  4, False),
        ([1,1,1,2,2,2,3,3,3],            3, True),
        ([1,2,3,4,5,6,7,8,9],            3, True),
        ([1,2,3,4,5,6,7,8,9],            4, False),
        ([1,2,3,4,5,6,7,8],              4, True),
        ([9,8,7,6,5,4,3,2,1,0],          5, True),
    ]

    approaches = [
        ("Brute Force (Sort+Counter)", canDivideIntoSets_brute),
        ("Optimal (Heap+Counter)",     canDivideIntoSets_heap),
        ("Optimal (Sorted Keys)",      canDivideIntoSets_sorted),
    ]

    all_passed = True
    for nums, k, expected in test_cases:
        for name, fn in approaches:
            result = fn(nums[:], k)
            status = "✓" if result == expected else "✗"
            if result != expected:
                all_passed = False
                print(f"  {status} FAIL | {name} | nums={nums}, k={k} | got {result}, expected {expected}")

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
# Approach                  Time          Space   Notes
# ──────────────────────────────────────────────────────────────────────────────
# Brute (Sort + Counter)    O(N log N)    O(N)    Simple, readable
# Optimal (Heap + Counter)  O(N log N)    O(N)    Explicit min tracking
# Optimal (Sorted Keys)     O(N log N)    O(N)    Cleanest; interview standard
#
# All three are the same asymptotic complexity.
# Sorted Keys is the go-to — Counter + sorted() + one greedy pass.
#
# ─────────────────────────────────────────────────────────────────────────────
# README — Heap Section Update
# ─────────────────────────────────────────────────────────────────────────────
#
# | # | Problem | Difficulty | Approach |
# |---|---------|------------|----------|
# | 1296 | Divide Array in Sets of K Consecutive Numbers | Medium | Same as LC 846;
# |      |                                               |        | Counter + sorted keys,
# |      |                                               |        | greedily consume from min |