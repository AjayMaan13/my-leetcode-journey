"""
LONGEST SUBSTRING WITH AT MOST K DISTINCT CHARACTERS

Problem Statement:
Given a string s and integer k, find the length of the longest substring
that contains at most k distinct characters.

Example 1: s="aababbcaacc", k=2 -> 6  ("aababb")
Example 2: s="abcddefg",    k=3 -> 4  ("bcdd" or "cdde" etc.)
Example 3: s="eceba",       k=2 -> 3  ("ece")

Constraints:
- 1 <= s.length <= 5 * 10^4
- 0 <= k <= 50

Key idea:
  Maintain a window [left, right] where the number of distinct characters <= k.
  When the window becomes invalid (distinct > k), shrink from the left.
"""

# ===== Brute Force =====
# Try every possible starting index and expand rightward.
# Stop expanding as soon as a (k+1)th distinct character is added.
# Time: O(n^2) | Space: O(k) — freq map holds at most k+1 keys at once

class SolutionBrute:
    def lengthOfLongestSubstringKDistinct(self, s, k):
        max_len = 0

        for i in range(len(s)):
            freq = {}                           # char -> count in current window

            for j in range(i, len(s)):
                freq[s[j]] = freq.get(s[j], 0) + 1

                if len(freq) > k:               # exceeded k distinct — no point continuing
                    break

                max_len = max(max_len, j - i + 1)

        return max_len


# ===== Optimal — Sliding Window =====
# Expand right pointer each step. When distinct chars exceed k,
# shrink from the left — remove one count at a time and delete key when it hits 0.
# We never need to re-scan the string; each character is added and removed at most once.
# Time: O(n) | Space: O(k)

class SolutionOptimal:
    def lengthOfLongestSubstringKDistinct(self, s, k):
        if k == 0 or not s:
            return 0

        freq   = {}     # char -> frequency in current window
        left   = 0
        maxLen = 0

        for right in range(len(s)):
            # Expand: add right character to window
            freq[s[right]] = freq.get(s[right], 0) + 1

            # Shrink: window has too many distinct chars — move left forward
            while len(freq) > k:
                freq[s[left]] -= 1
                if freq[s[left]] == 0:
                    del freq[s[left]]   # remove char entirely when count drops to 0
                left += 1

            # Record: window [left..right] is now valid
            maxLen = max(maxLen, right - left + 1)

        return maxLen


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    optimal = SolutionOptimal()

    test_cases = [
        ("aababbcaacc", 2, 6),
        ("abcddefg",    3, 4),
        ("eceba",       2, 3),
        ("aa",          1, 2),
        ("abc",         0, 0),
        ("abcadcacacaca", 3, 11),
    ]

    for s, k, expected in test_cases:
        r1 = brute.lengthOfLongestSubstringKDistinct(s, k)
        r2 = optimal.lengthOfLongestSubstringKDistinct(s, k)
        status = "PASS" if r1 == expected and r2 == expected else "FAIL"
        print(f"{status} s={s!r:15} k={k} -> brute={r1}, optimal={r2} (expected {expected})")
