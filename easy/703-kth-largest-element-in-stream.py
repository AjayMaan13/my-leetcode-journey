"""
703. Kth Largest Element in a Stream
https://leetcode.com/problems/kth-largest-element-in-a-stream/
Difficulty: Easy
Topics: Tree, Design, Binary Search Tree, Heap (Priority Queue), Data Streams

Problem:
    Maintain a stream of integers and return the kth largest element
    after each new value is added.

Examples:
    k=3, nums=[4,5,8,2]
    add(3)→4, add(5)→5, add(10)→5, add(9)→8, add(4)→8

Constraints:
    0 <= nums.length <= 10^4
    1 <= k <= nums.length + 1
    -10^4 <= nums[i], val <= 10^4
    At most 10^4 calls to add()
"""

import heapq


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BRUTE FORCE — Sorted List
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Keep all numbers in a list. On every add(), append and re-sort.
#   kth largest = element at index -(k) from the end (or sorted[-k]).
#
# Time:  __init__ O(N log N) | add O(N log N) per call  ← re-sort every time
# Space: O(N)
# ─────────────────────────────────────────────────────────────────────────────

class KthLargest_brute:
    def __init__(self, k, nums):
        self.k = k
        self.stream = sorted(nums)          # keep sorted at all times

    def add(self, val):
        self.stream.append(val)
        self.stream.sort()                  # O(N log N) every add
        return self.stream[-self.k]         # kth from end = kth largest


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR IDEA A — Max-Heap (negated) + pop k times
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Store all numbers as negatives in a min-heap (simulating a max-heap).
#   To get kth largest: pop k elements, the kth one is the answer,
#   then push all k back.
#
# Does heap[k-1] work instead of popping? NO.
#   A heap is NOT a sorted array. heap[0] is guaranteed to be the minimum,
#   but heap[1], heap[2], ... are in partial order only.
#   e.g. heap = [-8, -5, -4, -3, -2] — heap[2] = -4 might not be 3rd largest.
#   You MUST pop k times to reliably get the kth element.
#
# Does this approach work? YES, but it's slow:
#   add()  →  push O(log N), pop k times O(k log N), push k back O(k log N)
#   Total per add: O(k log N) — much worse than the size-k heap for large k.
#
# Time:  __init__ O(N log N) | add O(k log N) per call
# Space: O(N)
# ─────────────────────────────────────────────────────────────────────────────

class KthLargest_maxheap:
    def __init__(self, k, nums):
        self.k = k
        self.heap = [-n for n in nums]      # negate for max-heap simulation
        heapq.heapify(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, -val)

        # Pop k times to reach kth largest
        popped = []
        for _ in range(self.k):
            popped.append(heapq.heappop(self.heap))

        result = -popped[-1]                # kth pop = kth largest (negated)

        # Push all k elements back
        for v in popped:
            heapq.heappush(self.heap, v)

        return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: OPTIMAL — Min-Heap of Size k  ← your size-k idea
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Maintain a min-heap of exactly k elements — always the k largest seen.
#   heap[0] (the minimum of those k) = the kth largest overall.
#
# Why this works:
#   If we keep only the k largest numbers, the smallest among them
#   is by definition the kth largest in the entire stream.
#
# add() logic:
#   1. Push val onto the heap.
#   2. If heap grows beyond k, pop the minimum (it can't be kth largest).
#   3. heap[0] is always the answer.
#
# Visual trace — k=3, nums=[4,5,8,2]:
#   init: push all → heap=[2,4,5,8], trim to k=3 → heap=[4,5,8]
#                                                         ↑ kth largest = 4
#   add(3):  push 3 → [3,4,5,8], size=4>3, pop min(3) → [4,5,8], return 4
#   add(5):  push 5 → [4,5,5,8], size=4>3, pop min(4) → [5,5,8], return 5
#   add(10): push10 → [5,5,8,10],size=4>3, pop min(5) → [5,8,10],return 5
#   add(9):  push 9 → [5,8,9,10],size=4>3, pop min(5) → [8,9,10],return 8
#   add(4):  push 4 → [4,8,9,10],size=4>3, pop min(4) → [8,9,10],return 8
#
# Time:  __init__ O(N log k) | add O(log k) per call  ← optimal
# Space: O(k)  — heap never exceeds k elements
# ─────────────────────────────────────────────────────────────────────────────

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = []                      # min-heap of size k

        for n in nums:
            heapq.heappush(self.heap, n)
            if len(self.heap) > k:
                heapq.heappop(self.heap)    # discard anything outside top-k

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)        # evict smallest if overfull
        return self.heap[0]                 # min of top-k = kth largest


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    all_passed = True

    def check(label, got, expected):
        nonlocal all_passed
        if got != expected:
            all_passed = False
            print(f"  ✗ FAIL | {label} | got {got}, expected {expected}")

    classes = [
        ("Brute (Sort)",       KthLargest_brute),
        ("Max-Heap (pop k)",   KthLargest_maxheap),
        ("Optimal (size-k)",   KthLargest),
    ]

    for name, cls in classes:
        # LeetCode Example 1
        kl = cls(3, [4, 5, 8, 2])
        check(f"{name} ex1-a", kl.add(3),  4)
        check(f"{name} ex1-b", kl.add(5),  5)
        check(f"{name} ex1-c", kl.add(10), 5)
        check(f"{name} ex1-d", kl.add(9),  8)
        check(f"{name} ex1-e", kl.add(4),  8)

        # LeetCode Example 2
        kl = cls(4, [7, 7, 7, 7, 8, 3])
        check(f"{name} ex2-a", kl.add(2),  7)
        check(f"{name} ex2-b", kl.add(10), 7)
        check(f"{name} ex2-c", kl.add(9),  7)
        check(f"{name} ex2-d", kl.add(9),  8)

        # k=1 → always return the max
        kl = cls(1, [5, 3, 1])
        check(f"{name} k1-a", kl.add(10), 10)
        check(f"{name} k1-b", kl.add(2),  10)
        check(f"{name} k1-c", kl.add(15), 15)

        # Negative numbers
        # k=2, init=[-5,-3,-1] → top-2=[-3,-1], 2nd largest=-3
        # add(-2): pool top-2=[-2,-1], 2nd largest=-2
        # add(0):  pool top-2=[-1,0],  2nd largest=-1
        kl = cls(2, [-5, -3, -1])
        check(f"{name} neg-a", kl.add(-2), -2)
        check(f"{name} neg-b", kl.add(0),  -1)

        # Empty initial stream
        kl = cls(1, [])
        check(f"{name} empty", kl.add(7), 7)

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
# Approach              __init__        add()         Space
# ──────────────────────────────────────────────────────────────────────────────
# Brute (sort list)     O(N log N)      O(N log N)    O(N)
# Max-heap (pop k)      O(N log N)      O(k log N)    O(N)   works but slow for large k
# Optimal (size-k heap) O(N log k)      O(log k)      O(k)   ← best
#
# ─────────────────────────────────────────────────────────────────────────────
# README — Heap Section Update
# ─────────────────────────────────────────────────────────────────────────────
#
# | # | Problem | Difficulty | Approach |
# |---|---------|------------|----------|
# | 703 | Kth Largest Element in a Stream | Easy | Min-heap of size k;
# |     |                                 |      | heap[0] = kth largest; O(log k) per add |