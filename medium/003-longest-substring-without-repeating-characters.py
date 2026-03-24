"""
3. Longest Substring Without Repeating Characters

Find the length of the longest substring (contiguous) with all unique characters.

Example 1: s = "abcabcbb" -> 3  ("abc")
Example 2: s = "bbbbb"    -> 1  ("b")
Example 3: s = "pwwkew"   -> 3  ("wke")

Constraints:
- 0 <= s.length <= 5 * 10^4
- s consists of English letters, digits, symbols and spaces.

Key idea (sliding window):
  Maintain a window [l, r]. Expand r each step.
  When a duplicate is found, shrink l past the previous occurrence.
"""

# ===== Brute Force =====
# Check every substring — use a set to detect duplicates.
# Time: O(n^3) — O(n^2) substrings, O(n) each for set build | Space: O(n)

class SolutionBrute(object):
    def lengthOfLongestSubstring(self, s):
        n    = len(s)
        maxL = 0

        for i in range(n):
            seen = set()
            for j in range(i, n):
                if s[j] in seen:        # duplicate found — this window is invalid
                    break
                seen.add(s[j])
                maxL = max(maxL, j - i + 1)

        return maxL


# ===== My Solution — Sliding Window with HashMap =====
# Instead of resetting the window on a duplicate, jump l directly past
# the previous occurrence of the duplicate character.
# The seen dict maps each character to its LATEST seen index.
# l = max(l, seen[cur] + 1) prevents l from ever moving backward
# (important when the duplicate is outside the current window).
# Time: O(n) | Space: O(n)

class SolutionOptimal(object):
    def lengthOfLongestSubstring(self, s):
        if not s:
            return 0

        seen = {}   # char -> most recent index seen
        maxL = 0
        l    = 0    # left boundary of the current valid window

        for r in range(len(s)):
            cur = s[r]
            if cur in seen:
                l = max(l, seen[cur] + 1)   # Prevents l to move backward
            seen[cur] = r                   # update to latest index
            maxL = max(maxL, r - l + 1)

        return maxL


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    optimal = SolutionOptimal()

    test_cases = [
        ("abcabcbb", 3),
        ("bbbbb",    1),
        ("pwwkew",   3),
        ("",         0),
        (" ",        1),
        ("au",       2),
        ("dvdf",     3),
    ]

    for s, expected in test_cases:
        r1 = brute.lengthOfLongestSubstring(s)
        r2 = optimal.lengthOfLongestSubstring(s)
        status = "PASS" if r1 == expected and r2 == expected else "FAIL"
        print(f"{status} s={s!r:15} -> brute={r1}, optimal={r2} (expected {expected})")
