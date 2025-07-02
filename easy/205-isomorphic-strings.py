"""
205. Isomorphic Strings

Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be replaced to get t.

All occurrences of a character must be replaced with another character while preserving the order of characters. 
No two characters may map to the same character, but a character may map to itself.

Example 1:
Input: s = "egg", t = "add"
Output: True

Example 2:
Input: s = "foo", t = "bar"
Output: False

Example 3:
Input: s = "paper", t = "title"
Output: True

Constraints:
- 1 <= s.length <= 5 * 10^4
- t.length == s.length
- s and t consist of any valid ASCII character.
"""


class Solution(object):
    def isIsomorphic(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        sDict = {}
        tDict = {}
        
        for char in s:
            if char in sDict:
                sDict[char] += 1
            else:
                sDict[char] = 1
        
        for char in t:
            if char in tDict:
                tDict[char] += 1
            else:
                tDict[char] = 1
        
        return sDict == tDict


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ("egg", "add", True),
        ("foo", "bar", False),
        ("paper", "title", True),
        ("badc", "baba", False),
        ("ab", "aa", False),
    ]

    for s, t, expected in test_cases:
        result = sol.isIsomorphic(s, t)
        print(f"isIsomorphic({s!r}, {t!r}) = {result} (Expected: {expected})")
