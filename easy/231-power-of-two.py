"""
LeetCode 231: Power of Two

Problem:
Given an integer n, return true if it is a power of two. Otherwise, return false.
An integer n is a power of two if there exists an integer x such that n == 2^x.

Examples:
- n = 1  → True  (2^0 = 1)
- n = 16 → True  (2^4 = 16)
- n = 3  → False
"""

# ===== My Solution =====
class Solution(object):
    def isPowerOfTwo(self, n):
        if n <= 0:
            return False

        found = False
        i = 0
        while (1 << i) <= n:
            if n & (1 << i) != 0:
                if not found:
                    found = True
                else:
                    return False
            i += 1

        return True

# Time: O(log N), Space: O(1)
# Checks that exactly one bit is set by scanning all bits


# ===== Optimized Solution 1: Bit Trick =====
class Solution:
    def isPowerOfTwo(self, n):
        return n > 0 and (n & (n - 1)) == 0

# Time: O(1), Space: O(1)
# Power of two has exactly one bit set → n & (n-1) clears it to 0


# ===== Optimized Solution 2: Bit Count =====
class Solution:
    def isPowerOfTwo(self, n):
        return n > 0 and bin(n).count('1') == 1

# Time: O(log N), Space: O(1)
# Powers of two have exactly one '1' bit in binary representation
