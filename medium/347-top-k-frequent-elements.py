"""
347. Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/
Difficulty: Medium
Topics: Array, Hash Table, Divide and Conquer, Sorting, Heap (Priority Queue),
        Bucket Sort, Counting, Quickselect

Problem:
    Given integer array nums and integer k, return the k most frequent elements.
    Answer may be in any order.

Examples:
    nums = [1,1,1,2,2,3],          k = 2  →  [1, 2]
    nums = [1],                    k = 1  →  [1]
    nums = [1,2,1,2,1,2,3,1,3,2], k = 2  →  [1, 2]

Follow-up: Solve in better than O(N log N).

Constraints:
    1 <= nums.length <= 10^5
    -10^4 <= nums[i] <= 10^4
    k is in range [1, number of unique elements]
    Answer is guaranteed unique
"""

import heapq
from collections import Counter


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE — Sort by Frequency
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Count frequencies, sort all unique elements by frequency descending,
#   return first k.
#
# Time:  O(N log N)  — sorting U unique elements (U ≤ N)
# Space: O(N)        — counter + sorted list
# ─────────────────────────────────────────────────────────────────────────────

def topKFrequent_brute(nums, k):
    count = {}
    for n in nums:
        count[n] = 1 + count.get(n, 0)

    # Sort unique elements by frequency descending
    sorted_by_freq = sorted(count.keys(), key=lambda x: -count[x])
    return sorted_by_freq[:k]


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR SOLUTION — Max-Heap (negated frequencies)
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Count frequencies, push all (-freq, num) into a max-heap (via negation).
#   Pop k times — each pop gives the next most frequent element.
#
# Does it work? YES — clean and correct.
# Is it optimal? No — pushes ALL unique elements into the heap.
#   - If there are U unique elements, heap build is O(U log U).
#   - But we only need the top k. Approach 3 keeps heap size bounded at k.
#
# The `seen` set you declared was unused — Counter/dict handles deduplication.
#
# Time:  O(N + U log U + k log U)  ≈  O(N log N)  — heap over all uniques
# Space: O(U)  — heap holds all unique elements
# ─────────────────────────────────────────────────────────────────────────────

def topKFrequent_maxheap(nums, k):
    countMap = {}
    for num in nums:
        countMap[num] = 1 + countMap.get(num, 0)

    heap = []
    for key, count in countMap.items():
        heapq.heappush(heap, (-count, key))   # negate → max-heap

    res = []
    for _ in range(k):
        count, item = heapq.heappop(heap)
        res.append(item)

    return res


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: YOUR OPTIMAL — Min-Heap of Size k
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Count frequencies, then maintain a min-heap of exactly k elements.
#   The heap always holds the k most frequent elements seen so far.
#   When heap exceeds size k, pop the minimum-frequency element (it can't
#   be in the top k anymore). At the end, the heap IS the answer.
#
# Why this is better than the max-heap:
#   Max-heap: push ALL U unique elements, pop k times → O(U log U)
#   Min-heap of size k: push each of U elements once, pop if > k → O(U log k)
#   Since k ≤ U ≤ N, O(U log k) ≤ O(U log U) — better when k << N.
#
# Visual trace — nums=[1,1,1,2,2,3], k=2:
#   countMap = {1:3, 2:2, 3:1}
#   push (3,1) → heap=[(3,1)]
#   push (2,2) → heap=[(2,2),(3,1)], size=2 ≤ k, no pop
#   push (1,3) → heap=[(1,3),(3,1),(2,2)], size=3 > k=2, pop min=(1,3)
#   heap=[(2,2),(3,1)] → extract nums → [2, 1] ✓
#
# Time:  O(N + U log k)  — count O(N), heap ops O(U log k)
#        Since U ≤ N: O(N log k) overall  — satisfies follow-up O(N log N)
# Space: O(k)  — heap never exceeds k+1 elements
# ─────────────────────────────────────────────────────────────────────────────

def topKFrequent_minheap(nums, k):
    countMap = {}
    for num in nums:
        countMap[num] = 1 + countMap.get(num, 0)

    heap = []
    for num, count in countMap.items():
        heapq.heappush(heap, (count, num))     # min-heap by frequency

        if len(heap) > k:
            heapq.heappop(heap)                # evict least frequent

    return [num for count, num in heap]


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: BUCKET SORT — O(N), Truly Optimal
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Frequency of any element is between 1 and N (length of array).
#   Create N+1 buckets where bucket[f] holds all elements with frequency f.
#   Iterate buckets from high frequency to low, collect until we have k.
#
# No sorting, no heap — pure counting.
#
# Visual trace — nums=[1,1,1,2,2,3], k=2:
#   countMap = {1:3, 2:2, 3:1}
#   buckets:
#     [1] → [3]        (num 3 appears 1 time)
#     [2] → [2]        (num 2 appears 2 times)
#     [3] → [1]        (num 1 appears 3 times)
#   Scan right to left: freq=3→[1], freq=2→[2], stop at k=2
#   Result: [1, 2] ✓
#
# Time:  O(N)   — count + fill buckets + linear scan
# Space: O(N)   — buckets array of size N+1
# ─────────────────────────────────────────────────────────────────────────────

def topKFrequent_bucket(nums, k):
    countMap = {}
    for num in nums:
        countMap[num] = 1 + countMap.get(num, 0)

    # buckets[f] = list of numbers with frequency f
    # max frequency can be at most len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in countMap.items():
        buckets[freq].append(num)

    res = []
    # Scan from highest frequency to lowest
    for freq in range(len(buckets) - 1, 0, -1):
        for num in buckets[freq]:
            res.append(num)
            if len(res) == k:
                return res

    return res


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    test_cases = [
        # (nums, k, expected_set)  — order doesn't matter, check as sets
        ([1,1,1,2,2,3],             2, {1, 2}),
        ([1],                       1, {1}),
        ([1,2,1,2,1,2,3,1,3,2],    2, {1, 2}),
        ([4,4,4,6,6,5],             2, {4, 6}),
        ([1,2],                     2, {1, 2}),
        ([-1,-1,1,1,2],             2, {-1, 1}),
        ([1,1,1,2,2,3,3,3,3],       1, {3}),
        ([5,5,4,4,3,3],             3, {5, 4, 3}),    # all tied — any 3 valid
    ]

    approaches = [
        ("Brute (Sort)",       topKFrequent_brute),
        ("Max-Heap (yours)",   topKFrequent_maxheap),
        ("Min-Heap size-k",    topKFrequent_minheap),
        ("Bucket Sort O(N)",   topKFrequent_bucket),
    ]

    all_passed = True
    for nums, k, expected_set in test_cases:
        for name, fn in approaches:
            result = fn(nums[:], k)
            result_set = set(result)
            ok = (result_set == expected_set) and (len(result) == k)
            if not ok:
                all_passed = False
                print(f"  ✗ FAIL | {name} | nums={nums}, k={k} | got {result}, expected set {expected_set}")

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
# Approach              Time            Space   Follow-up O(N log N)?
# ──────────────────────────────────────────────────────────────────────────────
# Brute (Sort)          O(N log N)      O(N)    ✗ exactly N log N
# Max-Heap (all uniq)   O(N log N)      O(N)    ✗ heap over all uniques
# Min-Heap size k       O(N log k)      O(k)    ✓ better when k << N
# Bucket Sort           O(N)            O(N)    ✓ strictly linear
#
# Interview answer: mention all four, code min-heap O(N log k) or bucket O(N).
#
# ─────────────────────────────────────────────────────────────────────────────
# README — Heap Section Update
# ─────────────────────────────────────────────────────────────────────────────
#
# | # | Problem | Difficulty | Approach |
# |---|---------|------------|----------|
# | 347 | Top K Frequent Elements | Medium | Min-heap size k → O(N log k);
# |     |                         |        | Bucket sort → O(N); follow-up satisfied |