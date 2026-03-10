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
# For each candidate (num+1 and num+2), check every i from 1 to n.
# If i divides n, the pair is (i, n//i).
# Track the pair with the smallest absolute difference seen so far.
#
# Problem: for large num this scans millions of numbers — too slow.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def closestDivisors(self, num: int):
        best = None
        diff = float('inf')

        for n in [num + 1, num + 2]:
            for i in range(1, n + 1):       # try every possible divisor
                if n % i == 0:
                    a = i
                    b = n // i              # paired divisor

                    if abs(a - b) < diff:   # closer pair found → update best
                        diff = abs(a - b)
                        best = [a, b]

        return best


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: √N Scan (Improved)
# Time  : O(√N),  Space : O(1)
#
# Key insight — divisors come in pairs (i, n//i):
#   e.g. 36: (1,36), (2,18), (3,12), (4,9), (6,6)
#   Every pair has one factor ≤ √n and one ≥ √n.
#   So we only need to scan i from 1 up to √n to find ALL pairs.
#
# Unlike Approach 1 (which starts from 1 and must scan the full range),
# we scan i from 1 → √n, collecting every valid pair and comparing diffs.
# This cuts the work from O(N) → O(√N).
#
# Note: we still scan all pairs and compare — we don't stop early.
# That early-stop improvement comes in Approach 3.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def closestDivisors(self, num: int):
        best = None
        diff = float('inf')

        for n in [num + 1, num + 2]:
            i = 1
            while i * i <= n:               # only scan up to √n
                if n % i == 0:
                    a = i
                    b = n // i              # paired divisor (b >= a always)

                    if abs(a - b) < diff:   # this pair is closer → update best
                        diff = abs(a - b)
                        best = [a, b]

                i += 1

        return best


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: Start From √N (Optimal)
# Time  : O(√N),  Space : O(1)
#
# Key insight — the CLOSEST pair is always near √n:
#   e.g. 100: (1,100)diff=99, (2,50)diff=48, (4,25)diff=21, (5,20)diff=15,
#             (10,10)diff=0  ← best is the pair closest to the middle
#
# So instead of scanning UP from 1 and tracking the best so far,
# scan DOWN from √n — the FIRST divisor found immediately gives the
# closest pair for that target. No need to check the rest.
#
# Algorithm:
#   helper(n): scan i from √n downward, return first (i, n//i) where i|n.
#   Run helper for both num+1 and num+2, return the better of the two.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def closestDivisors(self, num: int):

        def helper(n):
            i = int(n ** 0.5)       # start at √n (the midpoint of all pairs)
            while i > 0:
                if n % i == 0:
                    return [i, n // i]  # first hit = closest pair for n
                i -= 1
            return [1, n]               # unreachable (i=1 always divides)

        a = helper(num + 1)
        b = helper(num + 2)

        # Compare the closest pair from each target, return the better one
        if abs(a[0] - a[1]) < abs(b[0] - b[1]):
            return a
        return b


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: Single-pass — both targets in one loop  ← CLEVEREST
# Time  : O(√N),  Space : O(1)
#
# Approach 3 runs two separate √N scans (one for num+1, one for num+2).
# This approach handles BOTH in a single downward scan from √(num+2).
#
# Key trick:
#   n = num + 2  (the larger target)
#   For each d from √n down to 1, check: does d divide n OR (n-1)?
#   Combined condition: n % d < 2
#     → n % d == 0  means d divides num+2
#     → n % d == 1  means d divides num+1  (since (num+2) leaving remainder 1
#                   means (num+1) leaving remainder 0)
#
#   Once the first d is found, decide which target it belongs to:
#     if (n-1) % d != 0  → d divides num+2    → return [d, n//d]
#     if (n-1) % d == 0  → d divides num+1    → return [d, (n-1)//d]
#
#   Why this gives the BEST answer overall:
#   Scanning from √n downward, the FIRST hit (across either target) gives
#   the pair with the smallest difference — because both targets are scanned
#   simultaneously at each d, so whichever yields a valid pair first wins.
#
# Trace for num=8:
#   n=10, start d=3
#   d=3: 10%3=1 < 2 → hit! (n-1)%d = 9%3 = 0 → d divides num+1=9
#        return [3, 9//3] = [3, 3]  ✓  (diff=0, beats num+2 pair [2,5] diff=3)
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def closestDivisors(self, num: int) -> list:
        n = num + 2
        for d in range(int(n ** 0.5), 0, -1):
            if n % d < 2:                               # d divides num+2 OR num+1
                return [d, n//d] if (n-1) % d else [d, (n-1)//d]
