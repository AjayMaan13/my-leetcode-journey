"""
LeetCode 22. Generate Parentheses  |  Medium

Problem Statement:
    Given n pairs of parentheses, generate all combinations of well-formed
    (valid) parentheses.

Examples:
    n = 1  →  ["()"]
    n = 3  →  ["((()))", "(()())", "(())()", "()(())", "()()()"]

Rules for a valid parentheses string:
    1. Every '(' must eventually be closed by a ')'
    2. A ')' can only be placed if there's an unmatched '(' before it
    3. Total '(' == Total ')' == n

Key Insight (Constraint):
    At any point while building the string:
      - We can add '('  if  openParen < n          (still have opens to place)
      - We can add ')'  if  closeParen < openParen  (unmatched opens exist)

    These two rules together guarantee only valid strings are built —
    no need to validate after the fact.
"""


# ─────────────────────────────────────────────────────────────────────────────
# YOUR SOLUTION  (cleaned up + fully commented)
# Time  : O(4^n / sqrt(n))  — Catalan number, the exact count of valid strings
# Space : O(n)              — recursion depth = 2n (max string length)
#
# Parameters:
#   openParen  — how many '(' have been placed so far
#   closeParen — how many ')' have been placed so far
#   curr       — the string being built
#   result     — collects all complete valid strings
#
# Recursion tree for n=2:
#
#                       ("", 0, 0)
#                      /
#                  ("(", 1, 0)
#                /              \
#         ("((", 2, 0)        ("()", 1, 1)
#              \              /          \
#         ("(()", 2, 1)  ("()(", 2, 1)  ← can't add ')' here, open=close
#              \               \
#         ("(())", 2, 2) ✓  ("()()", 2, 2) ✓
#
# Output (lexicographic because '(' < ')' and we always try '(' first):
#   ["(())", "()()"]
# ─────────────────────────────────────────────────────────────────────────────
def generateParenthesis(n: int) -> list:
    if n < 1:
        return []

    def generate(openParen: int, closeParen: int, curr: str, result: list) -> None:
        # Base case: placed n opens AND n closes → valid complete string
        if openParen == closeParen == n:
            result.append(curr)
            return

        # Branch 1: add '(' if we haven't used all n opens yet
        if openParen < n:
            generate(openParen + 1, closeParen, curr + "(", result)

        # Branch 2: add ')' only if there's an unmatched '(' waiting
        # openParen > closeParen means at least one '(' hasn't been closed
        if openParen > closeParen:
            generate(openParen, closeParen + 1, curr + ")", result)

    result = []
    generate(0, 0, "", result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# ALTERNATIVE: track remaining opens/closes instead of counts
# Same logic, different framing — easier to reason about for some people
#
# Instead of counting UP toward n, count DOWN from n toward 0:
#   open  = how many '(' we're still ALLOWED to place  (starts at n)
#   close = how many ')' we're still ALLOWED to place  (starts at n)
#
# Rules become:
#   add '('  if  open > 0
#   add ')'  if  close > open  (more closes remaining means unmatched opens exist)
# ─────────────────────────────────────────────────────────────────────────────
def generateParenthesis_remaining(n: int) -> list:
    if n < 1:
        return []

    result = []

    def generate(open_rem: int, close_rem: int, curr: str) -> None:
        # Base case: no more characters to place
        if open_rem == 0 and close_rem == 0:
            result.append(curr)
            return

        # Add '(' if we still have opens remaining
        if open_rem > 0:
            generate(open_rem - 1, close_rem, curr + "(")

        # Add ')' only if there are more closes remaining than opens
        # (close_rem > open_rem) means there are unmatched '(' that need closing
        if close_rem > open_rem:
            generate(open_rem, close_rem - 1, curr + ")")

    generate(n, n, "")
    return result
