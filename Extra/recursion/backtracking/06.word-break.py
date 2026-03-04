"""
PROBLEM: Word Break (LeetCode 139)
====================================

Given a string s and a dictionary of strings wordDict, return True if s can
be segmented into a space-separated sequence of one or more dictionary words.

Note: The same word in the dictionary can be used multiple times.

Examples:
    s = "takeuforward", wordDict = ["take","forward","you","u"]  → True
        "take" + "u" + "forward"

    s = "applepineapple", wordDict = ["apple"]                   → False
        "apple" + "pine" + "apple" — but "pine" not in dict

Constraints:
    - 1 <= s.length <= 300
    - 1 <= wordDict.length <= 1000
    - 1 <= wordDict[i].length <= 20
    - s and wordDict[i] consist of lowercase English letters
"""


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 1: Plain Recursion (your original)
# ─────────────────────────────────────────────────────────────────────────────
# At each position `start`, try every word in the dictionary.
# If the word matches at that position, recurse from after it.
# Base case: start == len(s) → entire string was consumed → True
#
# Problem: overlapping subproblems → same position recomputed many times
# 
# Time:  O(2^n)  — exponential without caching
# Space: O(n)    — recursion stack depth

def wordBreak_v1(s, wordDict):
    def solve(start):
        if start == len(s):         # used entire string
            return True

        for word in wordDict:
            end = start + len(word)
            if s[start:end] == word:    # does this word fit at `start`?
                if solve(end):          # recurse from right after it
                    return True

        return False                # no word worked from this position

    return solve(0)


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 2: Recursion + Memoization / Top-Down DP  (your optimised version)
# ─────────────────────────────────────────────────────────────────────────────
# Exact same recursion as above, but we cache the result at each `start`
# index so we never recompute the same position twice.
#
# WHY memo matters — without it, "aaaaaaab", wordDict=["a","aa","aaa"]:
#
#   solve(0)
#   ├── "a"   → solve(1)
#   │   ├── "a"  → solve(2)
#   │   │   ├── "a"   → solve(3)  ← computed many times below
#   │   │   ├── "aa"  → solve(4)  ← computed many times below
#   │   │   └── "aaa" → solve(5)  ← computed many times below
#   │   ├── "aa"  → solve(3) ← SAME solve(3) again  (wasteful)
#   │   └── "aaa" → solve(4) ← SAME solve(4) again  (wasteful)
#   ├── "aa"  → solve(2) ← SAME solve(2) again  (wasteful)
#   └── "aaa" → solve(3) ← SAME solve(3) again  (wasteful)
#
# With memo, each position 0..n is solved exactly ONCE → O(n * m) total.
#
# Time:  O(n * m * L)  — n positions × m words × L chars for slice compare
# Space: O(n)          — memo dict + recursion stack

def wordBreak_v2(s, wordDict):
    memo    = {}            # cache: start_index → True / False
    wordSet = set(wordDict) # set for O(1) lookup (vs O(m) list scan)

    def solve(start):
        if start == len(s):
            return True
        if start in memo:           # already solved this position
            return memo[start]

        for word in wordSet:
            end = start + len(word)
            if s[start:end] == word:
                if solve(end):
                    memo[start] = True
                    return True

        memo[start] = False         # nothing worked — cache the failure too
        return False

    return solve(0)


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION 3: Bottom-Up DP  ← canonical interview answer
# ─────────────────────────────────────────────────────────────────────────────
# dp[i] = True if s[0:i] can be formed from wordDict
#
# For every position i, look back at every word w:
#   if dp[i - len(w)] is True  AND  s[i-len(w) : i] == w
#   then dp[i] = True
#
# Visual for s = "takeuforward":
#
#  index:  0  1  2  3  4  5  6  7  8  9  10 11 12
#  char:      t  a  k  e  u  f  o  r  w  a  r  d
#  dp:    [T  F  F  F  T  T  F  F  F  F  F  F  T]
#                      ↑           ↑              ↑
#                    "take"       "u"         "forward"
#
# dp[0] = True (empty prefix — base case, 0 chars consumed = always valid)
# Final answer = dp[len(s)]
#
# Time:  O(n * m * L)  — same as memoized, but no recursion overhead
# Space: O(n)          — dp array only, no call stack

def wordBreak_v3(s, wordDict):
    n       = len(s)
    wordSet = set(wordDict)
    dp      = [False] * (n + 1)
    dp[0]   = True              # empty string is always "breakable"

    for i in range(1, n + 1):           # i = end of current substring s[0:i]
        for word in wordSet:
            wl = len(word)
            if i >= wl and dp[i - wl] and s[i - wl:i] == word:
                dp[i] = True
                break                   # no need to try more words for this i

    return dp[n]


# ─────────────────────────────────────────────────────────────────────────────
# Complexity summary
# ─────────────────────────────────────────────────────────────────────────────
#
#  Solution       Approach                Time           Space   Notes
#  ────────────  ──────────────────────  ─────────────  ──────  ──────────────
#  v1 (plain)    Recursion               O(2^n)         O(n)    TLE on large n
#  v2 (memo)     Top-down DP             O(n·m·L)       O(n)    Clean & fast
#  v3 (bottom)   Bottom-up DP            O(n·m·L)       O(n)    Best for interviews
#
#  n = len(s), m = len(wordDict), L = avg word length


# ─────────────────────────────────────────────────────────────────────────────
# Quick tests
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("takeuforward",   ["take","forward","you","u"],   True),
        ("applepineapple", ["apple"],                      False),
        ("leetcode",       ["leet","code"],                True),
        ("catsandog",      ["cats","dog","sand","and","cat"], False),
        ("aab",            ["a","aa","aab"],               True),
        ("aaaaaaab",       ["a","aa","aaa"],               False),
        ("",               ["a"],                          True),   # empty string
    ]

    for s, wordDict, expected in tests:
        r1 = wordBreak_v1(s, wordDict)
        r2 = wordBreak_v2(s, wordDict)
        r3 = wordBreak_v3(s, wordDict)
        assert r1 == expected, f"v1 failed: {s!r}"
        assert r2 == expected, f"v2 failed: {s!r}"
        assert r3 == expected, f"v3 failed: {s!r}"
        print(f"  s={s!r:20s}  expected={str(expected):5s}  ✓")

    print("\nAll test cases passed ✓")