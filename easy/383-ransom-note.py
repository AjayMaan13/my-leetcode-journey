"""
383. Ransom Note

Given two strings ransomNote and magazine, return true if ransomNote can be constructed 
by using the letters from magazine and false otherwise.

Each letter in magazine can only be used once in ransomNote.

Example 1:
Input: ransomNote = "a", magazine = "b"
Output: False

Example 2:
Input: ransomNote = "aa", magazine = "ab"
Output: False

Example 3:
Input: ransomNote = "aa", magazine = "aab"
Output: True

Constraints:
- 1 <= ransomNote.length, magazine.length <= 10^5
- ransomNote and magazine consist of lowercase English letters.
"""

# ✅ My Solution
class Solution(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        ransomDict = {}
        for char in ransomNote:
            if char in ransomDict:
                ransomDict[char] += 1
            else:
                ransomDict[char] = 1

        for char in magazine:
            if char in ransomDict and ransomDict[char] > 0:
                ransomDict[char] -= 1

        for value in ransomDict.values():
            if value != 0:
                return False

        return True


# ✅ Optimized Dictionary-Only Solution
class SolutionOptimized(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        dictionary = {}

        for char in magazine:
            if char not in dictionary:
                dictionary[char] = 1
            else:
                dictionary[char] += 1

        for char in ransomNote:
            if char in dictionary and dictionary[char] > 0:
                dictionary[char] -= 1
            else:
                return False

        return True


# ✅ Collections.Counter Solution
from collections import Counter

class SolutionWithCounter(object):
    def canConstruct(self, ransomNote, magazine):
        """
        :type ransomNote: str
        :type magazine: str
        :rtype: bool
        """
        ransom_count = Counter(ransomNote)
        magazine_count = Counter(magazine)

        for char, count in ransom_count.items():
            if magazine_count[char] < count:
                return False

        return True


# ✅ Main function to test all
if __name__ == "__main__":
    ransomNote_cases = [
        ("a", "b", False),
        ("aa", "ab", False),
        ("aa", "aab", True),
        ("abc", "aabbcc", True),
        ("abcd", "abc", False),
    ]

    print("Testing Your Solution:")
    sol = Solution()
    for ransomNote, magazine, expected in ransomNote_cases:
        result = sol.canConstruct(ransomNote, magazine)
        print(f"canConstruct({ransomNote!r}, {magazine!r}) = {result} (Expected: {expected})")

    print("\nTesting Optimized Dictionary Solution:")
    sol_opt = SolutionOptimized()
    for ransomNote, magazine, expected in ransomNote_cases:
        result = sol_opt.canConstruct(ransomNote, magazine)
        print(f"canConstruct({ransomNote!r}, {magazine!r}) = {result} (Expected: {expected})")

    print("\nTesting Collections.Counter Solution:")
    sol_counter = SolutionWithCounter()
    for ransomNote, magazine, expected in ransomNote_cases:
        result = sol_counter.canConstruct(ransomNote, magazine)
        print(f"canConstruct({ransomNote!r}, {magazine!r}) = {result} (Expected: {expected})")
