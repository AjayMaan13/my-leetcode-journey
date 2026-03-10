"""
LeetCode 1492. The kth Factor of n  |  Medium

Problem:
Given two positive integers n and k, return the kth factor of n in ascending
order, or -1 if n has fewer than k factors.
A factor of n is an integer i where n % i == 0.

Examples:
    n=12, k=3 → 3   (factors: 1,2,3,4,6,12 → 3rd is 3)
    n=7,  k=2 → 7   (factors: 1,7 → 2nd is 7)
    n=4,  k=4 → -1  (factors: 1,2,4 → only 3 factors)

Complexity Summary:
    Approach          Time    Space
    Brute Force       O(n)    O(1)
    √n with list      O(√n)   O(√n)
    Optimal √n        O(√n)   O(1)
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Brute Force
# Time  : O(n),  Space : O(1)
#
# Check every number from 1 to n.
# If i divides n, it's a factor — increment count.
# When count hits k, return i immediately.
# If we exhaust the loop without hitting k, return -1.
#
# Problem: if n = 1000 and k = 1, we still scan all the way to 1000.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def kthFactor(self, n: int, k: int) -> int:
        count = 0

        for i in range(1, n + 1):      # check every number from 1 to n
            if n % i == 0:              # i is a factor of n
                count += 1
                if count == k:          # found the kth factor
                    return i

        return -1                       # fewer than k factors exist


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: √n with List
# Time  : O(√n),  Space : O(√n)
#
# Key fact — divisors come in pairs (i, n//i):
#   e.g. 36: (1,36), (2,18), (3,12), (4,9), (6,6)
#   One factor in each pair is always ≤ √n, the other ≥ √n.
#   So scanning up to √n finds ALL divisors in half the iterations.
#
# To return them in ascending order we need both halves sorted correctly:
#   small[] = [1, 2, 3, 4, 6]    ← collected in ascending order (i goes up)
#   large[] = [36, 18, 12, 9, 6] ← collected in descending order (paired)
#   → reverse large to get [6, 9, 12, 18, 36]  (skip 6 if perfect square)
#   → concat: [1, 2, 3, 4, 6, 9, 12, 18, 36]  — fully sorted factors
#
# Then just index into the combined list.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def kthFactor(self, n: int, k: int):
        small = []
        large = []

        i = 1
        while i * i <= n:
            if n % i == 0:
                small.append(i)             # smaller factor of the pair

                if i != n // i:             # avoid duplicate at perfect square
                    large.append(n // i)    # larger factor of the pair

            i += 1

        # small is already ascending; large was added in ascending i order
        # so large is DESCENDING — reverse it to make it ascending
        factors = small + large[::-1]

        if k <= len(factors):
            return factors[k - 1]           # 1-indexed → subtract 1

        return -1


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: Optimal √n (No extra list)
# Time  : O(√n),  Space : O(1)
#
# Approach 2 is O(√n) time but uses O(√n) space to store factors.
# We can avoid storing anything by doing two passes without a list:
#
# Pass 1 (upward, i = 1 → √n):
#   Count factors in the "small" half (i ≤ √n).
#   If k is reached here, return i immediately.
#
# Pass 2 (downward, i = √n → 1):
#   The "large" factors are n//1, n//2, ..., n//√n — in descending order.
#   We continue counting from where Pass 1 left off.
#   When count hits k, return n//i (the large paired divisor).
#
# Special case: if n is a perfect square (i*i == n), its square root i was
# already counted in Pass 1, so we skip it in Pass 2 to avoid double-counting.
#
# e.g. n=36, k=7:
#   Pass 1: i=1(ct=1),2(ct=2),3(ct=3),4(ct=4),6(ct=5) → k not hit yet, i ends at 6
#   i*i=36==n → perfect square, skip i=6 in pass 2, start from i=5
#   Pass 2: i=5→36%5≠0; i=4→ct=6; i=3→ct=7 → return 36//3 = 12  ✓
#   (factors of 36 in order: 1,2,3,4,6,9,12,18,36 → 7th = 12)
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def kthFactor(self, n: int, k: int):
        count = 0
        i = 1

        # Pass 1: scan small factors (i up to √n)
        while i * i <= n:
            if n % i == 0:
                count += 1
                if count == k:
                    return i            # kth factor is in the small half
            i += 1

        # After the loop, i overshot by 1 — step back to the last value checked
        i -= 1

        # If n is a perfect square, i*i == n was already counted in Pass 1
        # → skip it in Pass 2 to avoid counting it twice
        if i * i == n:
            i -= 1

        # Pass 2: scan large factors (n//i for i going back down to 1)
        while i >= 1:
            if n % i == 0:
                count += 1
                if count == k:
                    return n // i       # kth factor is the paired large divisor
            i -= 1

        return -1                       # fewer than k factors exist
