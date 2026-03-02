"""
LeetCode 17. Letter Combinations of a Phone Number  |  Medium

Problem Statement:
    Given a string of digits 2-9, return all possible letter combinations
    that the number could represent (like a phone keypad).

Phone mapping:
    2→abc  3→def  4→ghi  5→jkl  6→mno  7→pqrs  8→tuv  9→wxyz

Examples:
    digits="23"  →  ["ad","ae","af","bd","be","bf","cd","ce","cf"]
    digits="2"   →  ["a","b","c"]
    digits=""    →  []

Key Insight:
    This is a CARTESIAN PRODUCT problem — combine every letter from digit[0]
    with every letter from digit[1], with every letter from digit[2], etc.

    For "23":  {a,b,c} × {d,e,f}  =  {ad,ae,af,bd,be,bf,cd,ce,cf}

    Two natural ways to build this:
      1. Recursion / Backtracking — at each digit index, loop through its
         letters, append one, recurse to next digit, backtrack (pop).
      2. Iterative expansion — start with [""], for each digit extend every
         existing prefix by each letter mapped to that digit.
"""


# ─────────────────────────────────────────────────────────────────────────────
# SHARED MAPPING (used by all solutions)
# ─────────────────────────────────────────────────────────────────────────────
MAPPING = {
    "2": "abc", "3": "def", "4": "ghi",
    "5": "jkl", "6": "mno", "7": "pqrs",
    "8": "tuv", "9": "wxyz"
}


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: YOUR V1 — Recursive Backtracking with list path
# Time  : O(4^n * n)  — 4^n combinations (7,9 have 4 letters), each length n
# Space : O(n)        — recursion depth = len(digits), path length = n
#
# At each index, loop over the letters mapped to digits[index].
# Append one letter, recurse to index+1, then pop (backtrack).
# When index reaches len(digits), a full combination is complete → save it.
#
# Recursion tree for "23":
#
#         solve(0, [])
#        /     |     \
#   [a]       [b]       [c]      ← letters from '2' (abc)
#   / | \    / | \    / | \
# [ad][ae][af][bd][be][bf][cd][ce][cf]  ← letters from '3' (def)
#  ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓   ✓  ← all valid, index==len(digits)
#
# Minor improvement over your original:
#   mapping values stored as strings ("abc") not lists (["a","b","c"]) —
#   iterating over a string and a list of chars behaves identically in Python.
# ─────────────────────────────────────────────────────────────────────────────
def letterCombinations_v1(digits: str) -> list:
    if not digits:
        return []

    def solve(index: int, path: list, result: list) -> None:
        # Base case: built one letter per digit → full combination
        if index == len(digits):
            result.append("".join(path))
            return

        # Loop over each letter mapped to the current digit
        for ch in MAPPING[digits[index]]:
            path.append(ch)              # choose
            solve(index + 1, path, result)  # explore
            path.pop()                   # backtrack (undo)

    result = []
    solve(0, [], result)
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: YOUR V2 — Iterative Expansion (BFS-style)  ← most Pythonic
# Time  : O(4^n * n)  — same total work
# Space : O(4^n * n)  — res holds all combinations simultaneously
#
# Start with res = [""] (one empty string).
# For each digit, expand every existing prefix by appending each of the
# digit's letters. Replace res with the expanded list.
#
# Trace for "23":
#   Start:     res = [""]
#   Digit '2': res = ["a","b","c"]               (""→a, ""→b, ""→c)
#   Digit '3': res = ["ad","ae","af","bd","be","bf","cd","ce","cf"]
#
# The list comprehension `[prefix + ch for prefix in res for ch in mapping[digit]]`
# is exactly a CARTESIAN PRODUCT written as one line.
#
# Why start with [""] not []?
#   If res=[], the comprehension produces nothing on the first iteration.
#   [""] acts as a neutral "empty prefix" — appending to "" gives just the letter.
# ─────────────────────────────────────────────────────────────────────────────
def letterCombinations_v2(digits: str) -> list:
    if not digits:
        return []

    res = [""]   # seed: one empty prefix to build from

    for digit in digits:
        # For every existing prefix, extend it with each letter for this digit
        # This replaces res entirely — old prefixes are consumed into new ones
        res = [prefix + ch for prefix in res for ch in MAPPING[digit]]

    return res


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: RECURSION — string passing (no backtracking needed)
# Time  : O(4^n * n)
# Space : O(4^n * n)  — each call creates a new string; O(n) call stack
#
# Instead of a mutable path list with push/pop, pass the growing string
# directly as a parameter. Strings are immutable → each branch automatically
# gets its own copy. No explicit backtracking needed, but creates more string
# objects in memory.
# ─────────────────────────────────────────────────────────────────────────────
def letterCombinations_v3(digits: str) -> list:
    if not digits:
        return []

    result = []

    def solve(index: int, curr: str) -> None:
        if index == len(digits):
            result.append(curr)
            return
        for ch in MAPPING[digits[index]]:
            solve(index + 1, curr + ch)   # new string per call — no undo needed

    solve(0, "")
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: itertools.product (for completeness — not for interviews)
# Time  : O(4^n * n)
# Space : O(4^n * n)
#
# The itertools.product function directly computes the cartesian product.
# Clean one-liner but relies on standard library — interviewers usually want
# you to implement the logic yourself.
# ─────────────────────────────────────────────────────────────────────────────
from itertools import product as iproduct

def letterCombinations_v4(digits: str) -> list:
    if not digits:
        return []
    return ["".join(combo) for combo in iproduct(*[MAPPING[d] for d in digits])]
