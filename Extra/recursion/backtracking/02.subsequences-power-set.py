"""
Power Set: Print All Possible Subsequences of a String  |  TUF Problem

Problem Statement:
    Given a string, find all possible subsequences (any subset of characters
    maintaining original order). Include the empty string.

    A subsequence keeps characters in relative order but doesn't require
    them to be contiguous.

Examples:
    "abc"  →  ["", "a", "b", "ab", "c", "ac", "bc", "abc"]  (2^3 = 8 total)
    "aa"   →  ["", "a", "a", "aa"]                           (2^2 = 4 total)

Key Insight:
    For a string of length n, every character has 2 choices: INCLUDE or EXCLUDE.
    That gives 2^n total subsequences (including the empty string "").
    These 2^n choices map perfectly to the binary numbers 0 → 2^n - 1.
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: BIT MANIPULATION
# Time  : O(n * 2^n)  — 2^n masks, each scanned across n bits
# Space : O(n * 2^n)  — storing all subsequences
#
# Idea: treat each number from 0 to 2^n - 1 as a bitmask.
#       Each bit position i tells us whether to include s[i].
#
# Example for "abc" (n=3), mask = 5  (binary: 101):
#   bit 0 set → include s[0] = 'a'
#   bit 1 off → skip    s[1] = 'b'
#   bit 2 set → include s[2] = 'c'
#   → subsequence = "ac"
#
# Full mask → subsequence mapping for "abc":
#   000 (0)  → ""
#   001 (1)  → "a"
#   010 (2)  → "b"
#   011 (3)  → "ab"
#   100 (4)  → "c"
#   101 (5)  → "ac"
#   110 (6)  → "bc"
#   111 (7)  → "abc"
# ─────────────────────────────────────────────────────────────────────────────
class SolutionBitmask:
    def getSubsequences(self, s: str) -> list:
        n = len(s)
        total = 1 << n          # 2^n  (bit-shift: faster than 2**n)
        subsequences = []

        for mask in range(total):       # iterate every possible bitmask
            subseq = []
            for i in range(n):
                if mask & (1 << i):     # check if bit i is set in mask
                    subseq.append(s[i]) # include s[i] in this subsequence
            subsequences.append("".join(subseq))

        return subsequences


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: RECURSION + BACKTRACKING
# Time  : O(n * 2^n)  — 2^n leaf nodes, each builds a string of length ≤ n
# Space : O(n)        — recursion depth = n, current list length ≤ n
#
# Idea: at each index, make a binary decision — exclude or include s[index].
#       Recurse both ways. At the end of the string, record what was built.
#
# Recursion tree for "abc":
#
#                         helper(0, [])
#                    /                    \
#           helper(1, [])           helper(1, [a])
#           /         \             /           \
#     helper(2,[])  helper(2,[b])  helper(2,[a]) helper(2,[a,b])
#      /    \         /    \         /    \          /      \
#   (3,[]) (3,[c]) (3,[b]) (3,[b,c])(3,[a]) (3,[a,c]) (3,[a,b]) (3,[a,b,c])
#    ""     "c"    "b"    "bc"     "a"   "ac"     "ab"   "abc"
#
# Backtracking: after the "include" recursive call, we pop the character
# so the list is clean for the next branch. This avoids copying the list
# at every level, saving memory.
# ─────────────────────────────────────────────────────────────────────────────
class SolutionRecursion:
    def helper(self, s: str, index: int, current: list, result: list) -> None:
        # Base case: processed all characters → record current subsequence
        if index == len(s):
            result.append("".join(current))
            return

        # Choice 1: EXCLUDE s[index] — don't add anything, just recurse
        self.helper(s, index + 1, current, result)

        # Choice 2: INCLUDE s[index]
        current.append(s[index])
        self.helper(s, index + 1, current, result)

        # Backtrack: remove s[index] so we don't affect other branches
        # (restores `current` to its state before this call)
        current.pop()

    def getSubsequences(self, s: str) -> list:
        result = []
        self.helper(s, 0, [], result)
        return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: RECURSION with string passing (no backtracking needed)
# Time  : O(n * 2^n)
# Space : O(n * 2^n)  — each call creates a new string; more memory than Approach 2
#
# Instead of maintaining a mutable list and backtracking,
# pass the current string directly as a parameter.
# Since strings are immutable in Python, each branch gets its own copy
# automatically — no manual undo needed.
#
# Cleaner to read, but uses more memory than the backtracking version
# because new string objects are created at every recursive call.
# ─────────────────────────────────────────────────────────────────────────────
def getSubsequences_string(s: str) -> list:
    result = []

    def helper(index: int, curr: str) -> None:
        if index == len(s):
            result.append(curr)
            return
        helper(index + 1, curr)            # exclude s[index]
        helper(index + 1, curr + s[index]) # include s[index] — new string, no undo needed

    helper(0, "")
    return result
