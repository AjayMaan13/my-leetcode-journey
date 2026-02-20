"""
242. VALID ANAGRAM

Problem Statement:
Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An anagram is a word or phrase formed by rearranging the letters of another word,
using all the original letters exactly once.

Example 1:
Input: s = "anagram", t = "nagaram"
Output: true

Example 2:
Input: s = "rat", t = "car"
Output: false

Example 3:
Input: s = "listen", t = "silent"
Output: true
"""

from collections import Counter


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (HASH MAP - GENERAL)
# ==============================================================================
# Time Complexity: O(n) where n is length of strings
# Space Complexity: O(k) where k is number of unique characters

class Solution_HashMap:
    def isAnagram(self, s, t):
        """
        Use hash map to count characters - works for any Unicode characters.
        
        Strategy:
        1. Count frequency of each character in s
        2. Decrement frequency for each character in t
        3. If any character missing or goes negative, not an anagram
        
        Advantages:
        - Works for Unicode (emoji, Chinese, etc.)
        - Clear logic, easy to understand
        - Flexible for follow-up questions
        
        This is the BEST GENERAL solution!
        """
        # Quick length check
        if len(s) != len(t):
            return False
        
        # Count characters in s
        char_count = {}
        for ch in s:
            char_count[ch] = 1 + char_count.get(ch, 0)
        
        # Decrement for characters in t
        for ch in t:
            # Character not in s or already used up
            if ch not in char_count or char_count[ch] == 0:
                return False
            else:
                char_count[ch] -= 1
                # Extra safety check (shouldn't happen with length check)
                if char_count[ch] < 0:
                    return False
        
        return True


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (ARRAY COUNT - LOWERCASE ONLY)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1) - fixed 26 character array

class Solution_ArrayCount:
    def isAnagram(self, s, t):
        """
        Use fixed-size array for lowercase letters only.
        
        Strategy:
        1. Create array of 26 zeros (for 'a' to 'z')
        2. Increment for each character in s
        3. Decrement for each character in t
        4. If all counts are 0, it's an anagram
        
        Advantages:
        - O(1) space (fixed 26 elements)
        - Slightly faster than hash map
        - Good for constraint: only lowercase letters
        
        Limitation:
        - Only works for lowercase English letters
        - Not suitable for Unicode or mixed case
        """
        if len(s) != len(t):
            return False
        
        # Array for 26 lowercase letters
        count = [0] * 26
        
        # Process both strings simultaneously
        for i in range(len(s)):
            # Increment for s[i], decrement for t[i]
            count[ord(s[i]) - ord('a')] += 1
            count[ord(t[i]) - ord('a')] -= 1
        
        # Check if all counts are 0
        for num in count:
            if num != 0:
                return False
        
        return True


# ==============================================================================
# APPROACH 3: SORTING (SIMPLE)
# ==============================================================================
# Time Complexity: O(n log n) - due to sorting
# Space Complexity: O(n) - for sorted strings

class Solution_Sorting:
    def isAnagram(self, s, t):
        """
        Sort both strings and compare.
        
        Key Insight: Anagrams have same characters in same frequencies.
        After sorting, anagrams become identical strings.
        
        Strategy:
        1. Sort both strings
        2. Compare sorted versions
        
        Advantages:
        - Simplest to code
        - Works for any characters
        - Easy to explain
        
        Disadvantage:
        - O(n log n) time (sorting)
        - Less efficient than counting approaches
        """
        return sorted(s) == sorted(t)


# ==============================================================================
# APPROACH 4: COUNTER (PYTHONIC)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(k) where k is unique characters

class Solution:
    def isAnagram(self, s, t):
        """
        Use Python's Counter from collections module.
        
        Counter is optimized hash map for counting.
        Most Pythonic solution!
        
        Advantages:
        - Cleanest code
        - Built-in optimization
        - Works for any characters
        - Shows Python expertise
        """
        return Counter(s) == Counter(t)

