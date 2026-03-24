"""
424. Longest Repeating Character Replacement

Given string s (uppercase letters) and integer k, you may change at most k
characters to any letter. Return the length of the longest substring that
contains only one distinct letter after those changes.

Example 1: s="ABAB",    k=2 -> 4  (replace both A's or both B's)
Example 2: s="AABABBA", k=1 -> 4  ("AABBBBA" — middle A replaced)

Constraints:
- 1 <= s.length <= 10^5
- s consists of only uppercase English letters
- 0 <= k <= s.length

Key insight:
  A window is valid when: (window size) - (max frequency in window) <= k
  i.e. the number of characters we'd need to replace fits within k.
"""

# ===== Brute Force =====
# Try every substring. For each, count frequencies and check validity.
# Window valid if: length - max(freq) <= k
# Time: O(n^2) | Space: O(26) = O(1)

class SolutionBrute(object):
    def characterReplacement(self, s, k):
        n    = len(s)
        maxL = 0

        for i in range(n):
            count = {}
            for j in range(i, n):
                count[s[j]] = count.get(s[j], 0) + 1

                # replacements needed = window length - count of most frequent char
                if (j - i + 1) - max(count.values()) <= k:
                    maxL = max(maxL, j - i + 1)
                else:
                    break   # extending further only makes it worse

        return maxL


# ===== My Solution — Sliding Window =====
# Maintain window [l, r]. Track maxFreq = highest char frequency seen in ANY window.
# Key trick: maxFreq never decreases — once we find a window of a certain size,
# we only care about finding a LARGER one, so we never need to shrink below that.
# Window invalid when: (r - l + 1) - maxFreq > k → slide l forward by 1.
# Time: O(n) | Space: O(26) = O(1)

class SolutionOptimal(object):
    def characterReplacement(self, s, k):
        if not s:
            return 0

        l       = 0
        maxFreq = 0   # max frequency seen across all windows (never decremented)
        maxL    = 0
        count   = {}

        for r in range(len(s)):
            count[s[r]] = 1 + count.get(s[r], 0)
            maxFreq = max(maxFreq, count[s[r]])     # update dominant char frequency

            # replacements needed exceeds k — slide window forward by 1
            if r - l + 1 - maxFreq > k:
                count[s[l]] -= 1
                l += 1

            maxL = max(maxL, r - l + 1)

        return maxL


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    optimal = SolutionOptimal()

    test_cases = [
        ("ABAB",    2, 4),
        ("AABABBA", 1, 4),
        ("AAAA",    2, 4),
        ("ABCD",    2, 3),
        ("A",       0, 1),
        ("AABBA",   1, 3),
    ]

    for s, k, expected in test_cases:
        r1 = brute.characterReplacement(s, k)
        r2 = optimal.characterReplacement(s, k)
        status = "PASS" if r1 == expected and r2 == expected else "FAIL"
        print(f"{status} s={s!r:12} k={k} -> brute={r1}, optimal={r2} (expected {expected})")
