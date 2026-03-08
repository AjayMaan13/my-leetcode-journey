"""
LeetCode 29. Divide Two Integers  |  Medium

Divide two integers without using multiplication, division, or mod operator.
Truncate toward zero. Clamp result to 32-bit signed integer range.

Examples:
    dividend = 10, divisor = 3  → 3   (10/3 = 3.333... → 3)
    dividend = 7, divisor = -3  → -2  (7/-3 = -2.333... → -2)

Constraints:
    -2^31 <= dividend, divisor <= 2^31 - 1
    divisor != 0
"""


# ─────────────────────────────────────────────────────────────────────────────
# MY SOLUTION: Bit-Shift Doubling
# Time  : O(log^2 N) — outer loop O(log N), inner loop O(log N)
# Space : O(1)
#
# Idea: Instead of subtracting divisor one at a time (O(N)), double it using
# left shifts until it exceeds dividend. Track how many times it fits (multiple).
# Repeat until dividend is exhausted. Handle sign separately.
#
# e.g. 10 / 3:
#   temp=3, multiple=1 → temp<<1=6 ≤ 10 → temp=6, multiple=2
#                       → temp<<1=12 > 10 → stop
#   dividend = 10-6=4, result=2
#   temp=3, multiple=1 → temp<<1=6 > 4 → stop
#   dividend = 4-3=1, result=3
#   1 < 3 → done. return 3 ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def divide(self, dividend, divisor):
        MAX_INT = 2**31 - 1
        MIN_INT = -2**31

        if dividend == MIN_INT and divisor == -1:
            return MAX_INT

        sign = -1 if (dividend < 0) ^ (divisor < 0) else 1

        dividend = abs(dividend)
        divisor = abs(divisor)

        result = 0

        while dividend >= divisor:
            temp = divisor
            multiple = 1

            while dividend >= (temp << 1):
                temp <<= 1
                multiple <<= 1

            dividend -= temp
            result += multiple

        return sign * result


# ─────────────────────────────────────────────────────────────────────────────
# OPTIMIZED: Single-pass bit manipulation (O(log N))
# Time  : O(log N)  — iterate over 31 bits once
# Space : O(1)
#
# Idea: Find the largest bit position where (divisor << i) fits into dividend,
# working from bit 31 down to 0. At each position, if it fits, subtract and
# record that bit in the result. This is essentially long division in binary.
#
# e.g. 10 / 3:
#   i=1: 3<<1=6 ≤ 10 → dividend=10-6=4, result |= 2  → result=2
#   i=0: 3<<0=3 ≤ 4  → dividend=4-3=1,  result |= 1  → result=3 ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        MAX_INT = 2**31 - 1
        MIN_INT = -2**31

        if dividend == MIN_INT and divisor == -1:
            return MAX_INT

        sign = -1 if (dividend < 0) ^ (divisor < 0) else 1
        a, b = abs(dividend), abs(divisor)

        result = 0
        for i in range(31, -1, -1):
            if (a >> i) >= b:
                result |= (1 << i)
                a -= b << i

        return sign * result
