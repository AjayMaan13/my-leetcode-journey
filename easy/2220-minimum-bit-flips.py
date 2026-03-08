"""
LeetCode 2220: Minimum Bit Flips to Convert Number

Problem:
Return the minimum number of bit flips to convert start to goal.
A bit flip changes a single bit from 0→1 or 1→0.

Examples:
- start=10 (1010), goal=7 (0111) → 3
- start=3  (011),  goal=4 (100)  → 3
"""

# ===== My Solution =====
class Solution(object):
    def minBitFlips(self, start, goal):
        count = 0

        while start > 0 or goal > 0:
            if (start & 1) != (goal & 1):
                count += 1
            start = start >> 1
            goal = goal >> 1

        return count

# Time: O(log N), Space: O(1)
# Checks each bit pair one at a time, counting mismatches


# ===== Optimized Solution: XOR + popcount =====
class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        return bin(start ^ goal).count('1')

# Time: O(log N), Space: O(1)
# XOR gives 1 wherever bits differ → count the 1s = number of flips needed
