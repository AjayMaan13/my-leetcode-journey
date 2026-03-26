"""
76. Minimum Window Substring

Given strings s and t, find the smallest substring of s that contains
every character in t (with duplicates). Return "" if none exists.

Example 1: s="ADOBECODEBANC", t="ABC"  -> "BANC"
Example 2: s="a",             t="a"    -> "a"
Example 3: s="a",             t="aa"   -> ""

Constraints:
- 1 <= s.length, t.length <= 10^5
- s and t consist of uppercase and lowercase English letters

Progression:
  Brute    → O(m^2 * n)  check every substring
  My sol   → O(m * n)    sliding window, but O(|t|) validity check per step
  Optimal  → O(m + n)    sliding window, O(1) validity via 'formed' counter
"""

# ===== Brute Force =====
# Try every substring of s. For each, check if it covers t using a freq map.
# Time: O(m^2 * n) — O(m^2) substrings, O(n) coverage check each | Space: O(n)

class SolutionBrute(object):
    def minWindow(self, s, t):
        required = {}
        for c in t:
            required[c] = required.get(c, 0) + 1

        result = ""

        for i in range(len(s)):
            freq = {}
            for j in range(i, len(s)):
                freq[s[j]] = freq.get(s[j], 0) + 1

                # check if window covers t
                covers = all(freq.get(c, 0) >= required[c] for c in required)
                if covers:
                    if not result or len(s[i:j+1]) < len(result):
                        result = s[i:j+1]
                    break   # no need to extend — already found shortest from i

        return result


# ===== My Solution — Sliding Window + valid() check =====
# Correct sliding window: expand r, shrink l whenever window is valid.
# Bottleneck: valid() iterates over all keys in requiredFreq each call → O(|t|)
# That makes the total O(m * |t|) instead of O(m).
# Time: O(m * n) | Space: O(m + n)

class SolutionMine(object):
    def minWindow(self, s, t):
        l      = 0
        freq   = {}
        maxStr = ""

        requiredFreq = {}
        for st in t:
            requiredFreq[st] = 1 + requiredFreq.get(st, 0)

        def valid(freq, requiredFreq):
            for key, value in requiredFreq.items():     # O(|t|) — called every step
                if key not in freq or freq[key] < value:
                    return False
            return True

        for r in range(len(s)):
            freq[s[r]] = 1 + freq.get(s[r], 0)

            while valid(freq, requiredFreq):            # valid() is O(|t|) here
                if not maxStr or len(maxStr) > r - l + 1:
                    maxStr = s[l:r + 1]
                freq[s[l]] -= 1
                l += 1

        return maxStr


# ===== Optimal — Sliding Window + 'formed' Counter =====
# Replace the O(|t|) valid() call with a single integer: 'formed'.
#
# required  = how many chars t needs and at what frequency
# formed    = how many of those requirements are currently satisfied
# need      = total number of unique chars t needs (len(required))
#
# When formed == need, the window is valid — try to shrink.
# Increment formed only when a char's count in window EXACTLY meets its requirement.
# Decrement formed only when a char's count drops BELOW its requirement.
# → validity check is O(1) per step.
# Time: O(m + n) | Space: O(m + n)

class SolutionOptimal(object):
    def minWindow(self, s, t):
        if not s or not t:
            return ""

        required = {}
        for c in t:
            required[c] = required.get(c, 0) + 1

        need   = len(required)   # number of unique chars we must satisfy
        formed = 0               # number of unique chars currently satisfied in window

        freq = {}
        l    = 0
        best = ""                # best (shortest) valid window found

        for r in range(len(s)):
            c = s[r]
            freq[c] = freq.get(c, 0) + 1

            # check if this char's requirement just became satisfied
            if c in required and freq[c] == required[c]:
                formed += 1

            # window is valid — try to shrink from left
            while formed == need:
                window = s[l:r + 1]
                if not best or len(window) < len(best):
                    best = window

                left_c = s[l]
                freq[left_c] -= 1
                if left_c in required and freq[left_c] < required[left_c]:
                    formed -= 1     # requirement no longer met — window becomes invalid
                l += 1

        return best


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    mine    = SolutionMine()
    optimal = SolutionOptimal()

    test_cases = [
        ("ADOBECODEBANC", "ABC",  "BANC"),
        ("a",             "a",    "a"),
        ("a",             "aa",   ""),
        ("AA",            "AA",   "AA"),
        ("cabwefgewcwaefgcf", "cae", "cwae"),
    ]

    for s, t, expected in test_cases:
        r1 = brute.minWindow(s, t)
        r2 = mine.minWindow(s, t)
        r3 = optimal.minWindow(s, t)
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected else "FAIL"
        print(f"{status} s={s!r:20} t={t!r:6} -> brute={r1!r}, mine={r2!r}, optimal={r3!r} (expected {expected!r})")
