"""
392. Is Subsequence

Given two strings s and t, return true if s is a subsequence of t, or false otherwise.

A subsequence of a string is a new string that is formed from the original string by deleting some 
(can be none) of the characters without disturbing the relative positions of the remaining characters. 
(i.e., "ace" is a subsequence of "abcde" while "aec" is not).

Example 1:
Input: s = "abc", t = "ahbgdc"
Output: True

Example 2:
Input: s = "axc", t = "ahbgdc"
Output: False

Constraints:
0 <= s.length <= 100
0 <= t.length <= 10^4
s and t consist only of lowercase English letters.

Follow up:
Suppose there are lots of incoming s, say s1, s2, ..., sk where k >= 10^9, and you want to check one by one to see if t has its subsequence. 
In this scenario, how would you change your code?
"""

class Solution(object):
    def isSubsequence(self, s, t):
        """
        Time: O(n) - constant time operation
        Space: O(1) - no extra space needed

        :type s: str
        :type t: str
        :rtype: bool
        """

        if len(s) > len(t):return False
        if len(s) == 0:return True

        sIndex,tIndex = 0

        tLength = len(t)
        sLength = len(s)

        while tIndex < tLength and sIndex < sLength:
            if s[sIndex] == t[tIndex]:
                sIndex += 1
            tIndex += 1

        return sIndex == len(s)


if __name__ == "__main__":
    sol = Solution()
    test_cases = [
        ("abc", "ahbgdc", True)
        ,
        ("axc", "ahbgdc", False),
        ("", "ahbgdc", True),
        ("ahbgdc", "ahbgdc", True),
        ("acb", "ahbgdc", False),  # order matters
    ]
    
    for s, t, expected in test_cases:
        result = sol.isSubsequence(s, t)
        print(f"isSubsequence({s!r}, {t!r}) = {result} (Expected: {expected})")
