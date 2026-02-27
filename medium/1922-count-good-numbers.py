"""
LeetCode 1922. Count Good Numbers  |  Medium

A digit string is "good" if:
  - Digits at EVEN indices (0, 2, 4, ...) are EVEN     → choices: 0,2,4,6,8  → 5 options
  - Digits at ODD  indices (1, 3, 5, ...) are PRIME    → choices: 2,3,5,7    → 4 options

Given an integer n, return the total number of good digit strings of length n,
modulo 10^9 + 7.

Examples:
    n = 1  → 5      (only index 0 = even, 5 choices)
    n = 4  → 400    (5^2 * 4^2 = 25 * 16 = 400)
    n = 50 → 564908303

Key Formula:
    even_positions = ceil(n/2) = (n+1)//2   ← indices 0,2,4,...
    odd_positions  = floor(n/2) = n//2       ← indices 1,3,5,...
    answer = 5^(even_positions) * 4^(odd_positions)  mod (10^9+7)
"""

MOD = 10 ** 9 + 7


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: ITERATIVE — loop through each position
# Time  : O(n)   — one loop iteration per position
# Space : O(1)
#
# Most straightforward — multiply in 5 or 4 depending on whether the
# current index is even or odd.
#
# Problem: for n = 10^15 this loop runs 10^15 times. Way too slow.
# Fine for small n, but NOT the intended solution.
# ─────────────────────────────────────────────────────────────────────────────
def countGoodNumbers_iterative(n: int) -> int:
    count = 1
    for i in range(n):
        if i % 2 == 0:
            count = (count * 5) % MOD   # even index → 5 even digit choices
        else:
            count = (count * 4) % MOD   # odd  index → 4 prime digit choices
    return count


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: NAIVE RECURSION
# Time  : O(n)   — one call per position, depth = n
# Space : O(n)   — call stack depth = n
#
# Recursively peel off one position at a time.
# n=4: countGoodNumbers(4) = 5 * countGoodNumbers(3)
#      countGoodNumbers(3) = 4 * countGoodNumbers(2)   (index 2 is even → 4? wait...)
#
# NOTE: this approach has a subtle flaw — it uses n's parity to decide the
# multiplier, but what we actually want is the parity of the CURRENT INDEX.
# Index = n-1, so when n is even the last index (n-1) is odd → multiply by 4.
# The recursion below works because when n reduces from 4 → 3 → 2 → 1 → 0,
# even n means the position at index n-1 is odd (prime slot = 4 choices),
# odd n means position n-1 is even (even-digit slot = 5 choices). ✓
#
# Still O(n) and hits RecursionError for large n.
# ─────────────────────────────────────────────────────────────────────────────
def countGoodNumbers_naive_recursive(n: int) -> int:
    if n == 0:
        return 1
    elif n % 2 == 0:
        # current last position (index n-1) is ODD  → 4 prime choices
        return (4 * countGoodNumbers_naive_recursive(n - 1)) % MOD
    else:
        # current last position (index n-1) is EVEN → 5 even-digit choices
        return (5 * countGoodNumbers_naive_recursive(n - 1)) % MOD


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: FAST POWER — ITERATIVE (Binary Exponentiation)
# Time  : O(log n)  — halving the exponent each step
# Space : O(1)      — no call stack, just variables
#
# Realise the answer is simply:  5^even_positions * 4^odd_positions  mod MOD
# Then use the same fast-power (binary exponentiation) trick from myPow:
#
#   base^exp:
#     while exp > 0:
#       if exp is odd → fold current base into result
#       square the base
#       halve the exp
#
# This is the cleanest production solution.
# ─────────────────────────────────────────────────────────────────────────────
def countGoodNumbers_fastpow_iterative(n: int) -> int:

    def fastPow(base: int, exp: int) -> int:
        result = 1
        base %= MOD
        while exp > 0:
            if exp % 2 == 1:                    # odd exponent: multiply in current base
                result = (result * base) % MOD
            base = (base * base) % MOD          # square the base
            exp //= 2                           # halve the exponent
        return result

    even_positions = (n + 1) // 2   # ceil(n/2)  — indices 0,2,4,...
    odd_positions  = n // 2         # floor(n/2) — indices 1,3,5,...

    part1 = fastPow(5, even_positions)  # 5 choices per even position
    part2 = fastPow(4, odd_positions)   # 4 choices per odd  position

    return (part1 * part2) % MOD


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: FAST POWER — RECURSIVE  🔥 (same logic as your optimised myPow)
# Time  : O(log n)
# Space : O(log n)  — call stack depth = log2(n)
#
# This is exactly your myPow problem in disguise:
#   x^n = (x^(n//2))^2           if n is even
#   x^n = (x^(n//2))^2 * x       if n is odd
#
# The only difference from myPow: every multiplication is wrapped with % MOD
# to prevent the number from growing astronomically large.
#
# Visual trace for fastPow(5, 3):
#
#   recPow(5, 3)   → n=3 is odd
#     half = recPow(5, 1)   → n=1 is odd
#              half = recPow(5, 0) → return 1
#            = (1 * 1 * 5) % MOD = 5
#     = (5 * 5 * 5) % MOD = 125
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def countGoodNumbers(self, n: int) -> int:

        def recPow(x: int, n: int) -> int:
            # Base case: x^0 = 1
            if n == 0:
                return 1

            # Compute x^(n//2) ONCE and store — same trick as optimised myPow
            half = recPow(x, n // 2)

            if n % 2 == 0:
                # x^n = (x^(n/2))^2
                return (half * half) % MOD
            else:
                # x^n = (x^(n/2))^2 * x
                # The extra *x handles the leftover factor when n is odd
                return (half * half * x) % MOD

        even_positions = (n + 1) // 2   # indices 0, 2, 4, ...  → 5 choices each
        odd_positions  = n // 2         # indices 1, 3, 5, ...  → 4 choices each

        part1 = recPow(5, even_positions)
        part2 = recPow(4, odd_positions)

        return (part1 * part2) % MOD

