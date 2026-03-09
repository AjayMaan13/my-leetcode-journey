"""
LeetCode 507: Perfect Number  |  Easy

Problem:
A perfect number equals the sum of its positive divisors, excluding itself.
Return true if num is a perfect number, otherwise false.

Examples:
    28 → True   (1 + 2 + 4 + 7 + 14 = 28)
    7  → False
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Brute Force
# Time  : O(N),  Space : O(1)
#
# Check every number from 1 to num-1, sum up the ones that divide evenly.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def checkPerfectNumber(self, num: int) -> bool:
        if num <= 1:
            return False
        total = 0
        for i in range(1, num):       # check every number below num
            if num % i == 0:
                total += i
        return total == num


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: Square Root Optimization  ← OPTIMAL
# Time  : O(√N),  Space : O(1)
#
# Key insight:
#   Divisors come in PAIRS: if i divides num, then (num // i) also divides num.
#   e.g. 28: pair (2,14), pair (4,7), and 1 is always a divisor.
#   So we only need to scan up to √num and add BOTH i and num//i at once.
#
#   Special case: if i == num // i (i.e. num is a perfect square like 36),
#   only count that divisor once to avoid doubling it.
#   Also never add num itself (the problem excludes it).
#
# Trace for num=28:
#   i=1: add 1 + 28  → but 28 == num, skip 28 → total=1
#   i=2: add 2 + 14  → total=17
#   i=3: 28%3 != 0   → skip
#   i=4: add 4 + 7   → total=28
#   i=5: 5*5=25 ≤ 28, 28%5 != 0 → skip
#   √28 ≈ 5.29, loop ends
#   total=28 == num → True ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def checkPerfectNumber(self, num: int) -> bool:
        if num <= 1:
            return False

        total = 1           # 1 is always a divisor (and never equals num for num>1)
        i = 2
        while i * i <= num:
            if num % i == 0:
                total += i                          # add the smaller divisor
                if i != num // i:                   # avoid double-counting square root
                    total += num // i               # add the paired larger divisor
            i += 1

        return total == num
