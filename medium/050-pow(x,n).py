"""
LeetCode 50. Pow(x, n)  |  Medium

Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).

Examples:
    Input: x = 2.00000, n = 10   → Output: 1024.00000
    Input: x = 2.10000, n = 3    → Output: 9.26100
    Input: x = 2.00000, n = -2   → Output: 0.25000  (2^-2 = 1/4)

Constraints:
    -100.0 < x < 100.0
    -2^31 <= n <= 2^31 - 1
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: NAIVE RECURSION  (your original solution)
# Time  : O(n)  — one recursive call per step, depth = n
# Space : O(n)  — call stack depth = n
#
# Idea: x^n = x * x^(n-1), unwind all the way down to base case n == 0.
#
# Problem: for large n (e.g. n = 2^31 - 1) this hits Python's recursion
# limit and is extremely slow. Fine for small inputs, not interview-ready.
# ─────────────────────────────────────────────────────────────────────────────
def myPow_naive(x: float, n: int) -> float:

    def recPow(x, n):
        # Base case: anything to the power 0 is 1
        if n == 0:
            return 1
        # Recurse: peel off one factor of x at a time
        return x * recPow(x, n - 1)

    if n == 0:
        return 1
    elif n < 0:
        # x^-n  =  1 / x^n
        # Convert negative exponent to positive, then invert the result
        return 1 / recPow(x, abs(n))
    else:
        return recPow(x, n)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: FAST POWER (Binary Exponentiation)  (your optimised solution)
# Time  : O(log n)  — we halve n on every even step → depth = log2(n)
# Space : O(log n)  — call stack depth = log2(n)
#
# Core insight — instead of multiplying x one at a time, square it:
#
#   x^n = (x^(n/2))^2          if n is even
#   x^n = x * x^(n-1)          if n is odd  (make it even, then use above)
#
# Visual trace for x=2, n=10:
#
#   recPow(2, 10)
#     └─ half = recPow(2, 5)
#                └─ 2 * recPow(2, 4)
#                         └─ half = recPow(2, 2)
#                                    └─ half = recPow(2, 1)
#                                               └─ 2 * recPow(2, 0)
#                                                          └─ 1
#                                              = 2 * 1 = 2
#                                    = 2 * 2 = 4        (half=2, half*half)
#                         = 4 * 4 = 16               (half=4, half*half)
#                = 2 * 16 = 32
#     = 32 * 32 = 1024  ✓
#
# Only 5 calls instead of 10 — and for n = 1,000,000,000 it's ~30 calls
# instead of a billion. That's the power of halving each time.
# ─────────────────────────────────────────────────────────────────────────────
def myPow(x: float, n: int) -> float:

    def recPow(x, n):
        # Base case: x^0 = 1 for any x
        if n == 0:
            return 1

        if n % 2 == 0:
            # EVEN exponent: compute x^(n/2) ONCE, then square it.
            # Crucial: store in `half` so we don't recompute it twice.
            # e.g. x^8 = (x^4)^2  →  compute x^4 once, multiply by itself
            half = recPow(x, n // 2)
            return half * half
        else:
            # ODD exponent: strip one factor of x, making the exponent even.
            # e.g. x^9 = x * x^8  →  now x^8 is even, hits the branch above
            return x * recPow(x, n - 1)

    if n == 0:
        return 1
    elif n < 0:
        # Negative exponent: x^-n = 1 / x^n
        # e.g. 2^-2 = 1 / 2^2 = 1 / 4 = 0.25
        return 1 / recPow(x, abs(n))
    else:
        return recPow(x, n)


# ─────────────────────────────────────────────────────────────────────────────
# BONUS: ITERATIVE fast power (O(log n) time, O(1) space — no call stack)
#
# Same binary exponentiation idea, but uses bit manipulation instead of
# recursion. Useful to know for follow-up interview questions.
#
# How it works:
#   Treat n in binary. Each bit tells you whether to multiply the current
#   power of x into the result.
#
#   e.g. n = 10  →  binary 1010
#        bit 1 (value 2^1):  result *= x^2   → result = 4
#        bit 3 (value 2^3):  result *= x^8   → result = 4 * 256 = 1024  ✓
#
#   We scan bits right-to-left by repeatedly doing n >>= 1 (right-shift).
#   At each step we square x (x = x*x) and if the current bit is 1 we
#   fold that power into result.
# ─────────────────────────────────────────────────────────────────────────────
def myPow_iterative(x: float, n: int) -> float:
    if n < 0:
        x = 1 / x   # flip base for negative exponent
        n = -n

    result = 1.0
    while n:
        if n & 1:           # if current lowest bit is set, multiply in x
            result *= x
        x *= x              # square x for the next bit position
        n >>= 1             # shift n right to examine the next bit
    return result

