"""
Palindrome Partitioning  |  TUF / LeetCode 131  |  Medium

Problem Statement:
    Given a string s, partition s such that every substring of the partition
    is a palindrome. Return all possible palindrome partitions.

Examples:
    s = "aabaa"  →  [["a","a","b","a","a"], ["a","a","b","aa"], ["a","aba","a"],
                     ["aa","b","a","a"], ["aa","b","aa"], ["aabaa"]]
    s = "baa"    →  [["b","a","a"], ["b","aa"]]
    s = "aab"    →  [["a","a","b"], ["aa","b"]]

Key Insight — Combination Sum / Subsets pattern, with a VALIDITY GATE:
    At each `start` position, try every possible end position.
    Only recurse deeper if s[start:end+1] is a palindrome — this is the gate.
    When start reaches the end of the string, we've covered every character
    with valid palindrome substrings → save the current partition.

    This is the SAME loop-based backtracking skeleton you've used before:
      for i in range(start, len(s)):
          if VALID(s[start:i+1]):       ← palindrome check = the constraint
              path.append(s[start:i+1])
              solve(i+1, path)
              path.pop()

    Compare to previous problems:
      Comb. Sum II  → constraint: candidates[i] <= remaining
      Subsets II    → constraint: no duplicate at same level
      Palindrome    → constraint: substring must be a palindrome
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: YOUR SOLUTION  (optimal — fully commented)
# Time  : O(n * 2^n)  — at most 2^n partitions, each palindrome check O(n)
# Space : O(n)        — recursion depth = n, path length = n
#
# isPalindrome uses two pointers instead of s[l:r+1] == s[l:r+1][::-1]
# to avoid creating a new reversed string — O(n) but no extra allocation.
# ─────────────────────────────────────────────────────────────────────────────
def partition_v1(s: str) -> list:
    result = []

    def isPalindrome(left: int, right: int) -> bool:
        """Two-pointer palindrome check on the original string s[left..right]."""
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def solve(start: int, path: list) -> None:
        # Base case: covered every character → valid complete partition found
        if start == len(s):
            result.append(path[:])   # snapshot the current partition
            return

        # Try every possible END position for the next substring
        for end in range(start, len(s)):
            # Only recurse if s[start..end] is a palindrome (the validity gate)
            # This prunes the tree early — invalid substrings are never explored
            if isPalindrome(start, end):
                path.append(s[start:end + 1])    # choose this palindrome substring
                solve(end + 1, path)             # recurse: find partitions for the rest
                path.pop()                       # backtrack: undo the choice

    solve(0, [])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: SAME LOGIC — but inline palindrome check (no helper function)
# Functionally identical to V1. Some prefer this for brevity in interviews.
# ─────────────────────────────────────────────────────────────────────────────
def partition_v2(s: str) -> list:
    result = []

    def solve(start: int, path: list) -> None:
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start, len(s)):
            sub = s[start:end + 1]
            if sub == sub[::-1]:           # palindrome check: string == its reverse
                path.append(sub)
                solve(end + 1, path)
                path.pop()

    solve(0, [])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: DP PRECOMPUTATION — O(n^2) preprocessing for O(1) palindrome check
# Time  : O(n^2) preprocessing + O(n * 2^n) backtracking
#         For strings with many palindromes, the O(1) lookup saves time vs
#         re-checking the same substrings repeatedly.
# Space : O(n^2) — DP table
#
# dp[i][j] = True if s[i..j] is a palindrome.
# Fill using the recurrence:
#   dp[i][j] = (s[i] == s[j]) AND dp[i+1][j-1]
# Base cases:
#   dp[i][i]   = True           (single char is always a palindrome)
#   dp[i][i+1] = (s[i]==s[i+1]) (two chars: palindrome iff equal)
# ─────────────────────────────────────────────────────────────────────────────
def partition_v3(s: str) -> list:
    n = len(s)

    # Precompute palindrome table: dp[i][j] = True if s[i..j] is a palindrome
    dp = [[False] * n for _ in range(n)]

    # Every single character is a palindrome
    for i in range(n):
        dp[i][i] = True

    # Fill for increasing lengths
    for length in range(2, n + 1):           # substring length
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 2:
                dp[i][j] = (s[i] == s[j])   # "aa" → True, "ab" → False
            else:
                # s[i..j] is palindrome iff outer chars match AND inner is palindrome
                dp[i][j] = (s[i] == s[j]) and dp[i + 1][j - 1]

    result = []

    def solve(start: int, path: list) -> None:
        if start == n:
            result.append(path[:])
            return

        for end in range(start, n):
            if dp[start][end]:              # O(1) palindrome check using precomputed table
                path.append(s[start:end + 1])
                solve(end + 1, path)
                path.pop()

    solve(0, [])
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Recursion trace for "aab" (from the problem description — confirmed correct)
#
# solve(0, [])
#   end=0: "a" ✅ palindrome
#     solve(1, ["a"])
#       end=1: "a" ✅
#         solve(2, ["a","a"])
#           end=2: "b" ✅
#             solve(3, ["a","a","b"]) → start==len → SAVE ✅
#       end=2: "ab" ❌ skip
#   end=1: "aa" ✅ palindrome
#     solve(2, ["aa"])
#       end=2: "b" ✅
#         solve(3, ["aa","b"]) → start==len → SAVE ✅
#   end=2: "aab" ❌ skip
# Result: [["a","a","b"], ["aa","b"]]  ✅
# ─────────────────────────────────────────────────────────────────────────────

