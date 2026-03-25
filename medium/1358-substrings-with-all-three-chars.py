# 1358. Number of Substrings Containing All Three Characters (Medium)
# Tags: Sliding Window, String, Hash Map
#
# Given a string s of only 'a', 'b', 'c', return the count of substrings
# that contain at least one of each character.
#
# Example: s = "abcabc" → 10


# ─────────────────────────────────────────────
# BRUTE FORCE — O(n²) time, O(1) space
# ─────────────────────────────────────────────
# Fix a left boundary, expand right, track counts of a/b/c.
# As soon as the window contains all three, every further extension
# is also valid → add (n - r) substrings and move to next left.
# Still O(n²) because we restart the scan for every left.

class Solution(object):
    def numberOfSubstrings(self, s):
        n = len(s)
        count = 0

        for l in range(n):
            freq = {'a': 0, 'b': 0, 'c': 0}

            for r in range(l, n):
                freq[s[r]] += 1

                # once all three present, every substring ending at r+1..n is valid
                if freq['a'] and freq['b'] and freq['c']:
                    count += n - r
                    break   # no need to extend further from this l

        return count


# ─────────────────────────────────────────────
# FIRST SOLUTION — Shrinkable Sliding Window — O(n) time, O(1) space
# ─────────────────────────────────────────────
# Expand r to the right; when the window [l..r] first holds all 3 chars:
#   - Every superstring of this window (i.e., extending r further to the right)
#     is also valid. There are (n - r) such substrings → add them all at once.
#   - Then shrink from the left (l++) to find MORE valid windows starting later.
# Repeat until the window no longer has all 3, then expand r again.
#
# Why count += (n - r)?
#   The substring s[l..r] is valid. Appending any suffix s[r+1], s[r+2], ..., s[n-1]
#   keeps it valid (more chars can't remove existing ones). That's (n - r) substrings.

class Solution2(object):
    def numberOfSubstrings(self, s):
        a = b = c = 0   # frequency counters for the current window
        l = 0
        count = 0

        for r in range(len(s)):
            # expand window by including s[r]
            if s[r] == 'a':   a += 1
            elif s[r] == 'b': b += 1
            else:              c += 1

            # shrink from left as long as all 3 are present
            while a and b and c:
                count += len(s) - r   # s[l..r], s[l..r+1], ..., s[l..n-1] all valid
                if s[l] == 'a':   a -= 1
                elif s[l] == 'b': b -= 1
                else:              c -= 1
                l += 1

        return count


# ─────────────────────────────────────────────
# OPTIMAL — Last-seen index trick — O(n) time, O(1) space
# ─────────────────────────────────────────────
# For each position r, track the LAST index where each of a, b, c was seen.
# The earliest of those three last-seen positions (call it `mn`) tells us:
#   every left boundary from 0..mn can pair with r to form a valid substring.
# So the count of valid substrings ending at r is exactly (mn + 1).
#
# Why (mn + 1)?
#   With last = {'a': la, 'b': lb, 'c': lc} and mn = min(la, lb, lc),
#   starting at any index 0..mn includes all three characters up to r.
#   That's mn+1 choices for the left endpoint, each giving a valid substring.

class Solution3(object):
    def numberOfSubstrings(self, s):
        last = {'a': -1, 'b': -1, 'c': -1}   # last seen index of each char
        count = 0

        for r, ch in enumerate(s):
            last[ch] = r   # update last seen

            # min of last-seen positions = rightmost "earliest" required char
            mn = min(last['a'], last['b'], last['c'])

            # mn == -1 means we haven't seen all 3 yet → contribute 0
            # otherwise, substrings starting at indices 0..mn with right at r are valid
            count += mn + 1

        return count
