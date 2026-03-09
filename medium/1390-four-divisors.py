"""
LeetCode 1390. Four Divisors  |  Medium

Problem:
Given an integer array nums, return the sum of divisors of integers that have
exactly four divisors. Return 0 if no such integer exists.

Examples:
    [21, 4, 7] → 32   (21 has divisors 1,3,7,21 → sum=32; others don't qualify)
    [21, 21]   → 64
    [1,2,3,4,5]→ 0
"""


# ─────────────────────────────────────────────────────────────────────────────
# MY SOLUTION: √N scan per number
# Time  : O(N * √M)  where M = max value in nums
# Space : O(1)
#
# For each number, find all divisors by scanning up to √num.
# Divisors come in pairs (i, num//i). Early exit if we already have > 4.
# Return sum only if exactly 4 divisors found.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def sumFourDivisors(self, nums):
        if not nums:
            return 0

        def divisors(num):
            if num < 6:         # smallest number with 4 divisors is 6 (1,2,3,6)
                return 0

            res = [1, num]      # 1 and num itself are always divisors
            i = 2
            while i * i <= num:
                if num % i == 0:
                    res.append(i)
                    if i != num // i:       # avoid double-counting perfect squares
                        res.append(num // i)
                    if len(res) > 4:        # already exceeded 4, stop early
                        return 0
                i += 1

            return sum(res) if len(res) == 4 else 0

        total = 0
        for num in nums:
            total += divisors(num)

        return total


# ─────────────────────────────────────────────────────────────────────────────
# OPTIMIZED: Early exit as soon as divisor count exceeds 4
# Time  : O(N * √M),  Space : O(1)
#
# Same √N scan but tighter: track count and sum directly (no list allocation).
# The moment we find a 3rd "inner" divisor (meaning count would exceed 4),
# immediately return 0 for that number. This avoids building a list at all.
#
# A number has exactly 4 divisors in two cases:
#   Case 1: n = p^3  → divisors are 1, p, p^2, p^3  (e.g. 8 = 2^3)
#   Case 2: n = p*q  → divisors are 1, p, q, p*q     (e.g. 21 = 3*7)
#
# In both cases the √N loop finds exactly ONE inner divisor pair.
# If it finds a second inner pair, count > 4 → not valid.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def sumFourDivisors(self, nums):
        total = 0

        for num in nums:
            div_sum = 1 + num       # always include 1 and num
            count = 2
            i = 2

            while i * i <= num:
                if num % i == 0:
                    count += 1
                    div_sum += i
                    if i != num // i:
                        count += 1
                        div_sum += num // i
                    if count > 4:   # exceeded 4 divisors, abandon this number
                        div_sum = 0
                        break
                i += 1

            if count == 4:
                total += div_sum

        return total
