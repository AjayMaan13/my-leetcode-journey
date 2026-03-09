"""
LeetCode 1362. Closest Divisors  |  Medium

Problem:
Given num, find two integers with the smallest absolute difference whose
product equals num+1 or num+2. Return them in any order.

Examples:
    num = 8   → [3, 3]   (9 = 3*3, diff=0; 10 = 2*5, diff=3 → pick 3,3)
    num = 123 → [5, 25]  (124 = 4*31 diff=27; 125 = 5*25 diff=20 → pick 5,25)
    num = 999 → [40, 25] (1000 = 40*25, diff=15 wins)
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Brute Force
# Time  : O(N),  Space : O(1)
#
# For each candidate (num+1, num+2), collect ALL divisor pairs, then pick
# the one with the smallest absolute difference.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def closestDivisors(self, num: int) -> list:
        best = None
        best_diff = float('inf')

        for target in (num + 1, num + 2):
            for i in range(1, target + 1):          # check every i from 1 to target
                if target % i == 0:
                    j = target // i
                    diff = abs(i - j)
                    if diff < best_diff:
                        best_diff = diff
                        best = [i, j]

        return best


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: √N Scan  ← OPTIMAL
# Time  : O(√N),  Space : O(1)
#
# Key insight:
#   Divisor pairs (i, n//i) get CLOSER together as i approaches √n.
#   So if we scan i from √n DOWN to 1, the FIRST valid pair we find
#   is already the closest pair for that target — no need to check the rest.
#
#   e.g. target=9, √9=3: i=3 → 9%3==0 → pair (3,3), diff=0. Stop immediately.
#   e.g. target=10, √10≈3: i=3 → 10%3≠0; i=2 → pair (2,5), diff=3. Stop.
#
# Algorithm:
#   1. For each of num+1 and num+2, find its closest divisor pair in O(√N).
#   2. Compare the two pairs and return whichever has the smaller difference.
# ─────────────────────────────────────────────────────────────────────────────
import math

class Solution:
    def closestDivisors(self, num: int) -> list:

        def closest_pair(target):
            # Start from √target and scan downward.
            # First i that divides target gives the closest pair (i, target//i).
            i = int(math.sqrt(target))
            while i >= 1:
                if target % i == 0:
                    return [i, target // i]     # closest pair found
                i -= 1

        pair1 = closest_pair(num + 1)
        pair2 = closest_pair(num + 2)

        # Return whichever pair has the smaller absolute difference
        if abs(pair1[0] - pair1[1]) <= abs(pair2[0] - pair2[1]):
            return pair1
        return pair2
