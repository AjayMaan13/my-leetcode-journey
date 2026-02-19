"""
796. ROTATE STRING

Problem Statement:
Given two strings s and goal, return true if and only if s can become goal 
after some number of shifts on s.

A shift on s consists of moving the leftmost character of s to the rightmost 
position.

Example 1:
Input: s = "abcde", goal = "cdeab"
Output: true
Explanation: After 2 shifts: "abcde" → "bcdea" → "cdeab"

Example 2:
Input: s = "abcde", goal = "abced"
Output: false

Example 3:
Input: s = "abcde", goal = "eabcd"
Output: true
Explanation: After 4 shifts: "abcde" → "bcdea" → "cdeab" → "deabc" → "eabcd"
"""


# ==============================================================================
# APPROACH 1: YOUR SOLUTION (STRING CONCATENATION - OPTIMAL)
# ==============================================================================
# Time Complexity: O(n) - string search is O(n) with good algorithms
# Space Complexity: O(n) - creating doubled string

class Solution:
    def rotateString(self, s, goal):
        """
        Brilliant trick: All rotations of s are substrings of s+s!
        
        Key Insight:
        If we concatenate s with itself (s+s), all possible rotations of s
        will appear as substrings in this doubled string.
        
        Example:
        s = "abcde"
        s+s = "abcdeabcde"
        
        All rotations of s:
        - "abcde" ✓ (substring at index 0)
        - "bcdea" ✓ (substring at index 1)
        - "cdeab" ✓ (substring at index 2)
        - "deabc" ✓ (substring at index 3)
        - "eabcd" ✓ (substring at index 4)
        
        So just check: goal in (s+s) and len(s) == len(goal)
        
        This is the STANDARD OPTIMAL solution!
        """
        # Must have same length to be rotations
        if len(s) != len(goal):
            return False
        
        # Empty strings are considered rotations of each other
        if not s and not goal:
            return True
        
        # Check if goal is substring of s+s
        return goal in s + s


# ==============================================================================
# APPROACH 2: CLEANER ONE-LINER VERSION
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n)

class Solution_OneLiner:
    def rotateString(self, s, goal):
        """
        Same algorithm but as elegant one-liner.
        
        Combines both checks in single expression:
        1. Length check: len(s) == len(goal)
        2. Rotation check: goal in (s + s)
        
        Note: When len(s) == len(goal), we know both are non-empty
        or both are empty, so the check works for all cases.
        """
        return len(s) == len(goal) and goal in s + s


# ==============================================================================
# APPROACH 3: SIMULATION (BRUTE FORCE)
# ==============================================================================
# Time Complexity: O(n²) - n rotations, each O(n) comparison
# Space Complexity: O(n) - storing rotated string

class Solution_Simulation:
    def rotateString(self, s, goal):
        """
        Simulate all possible rotations and check each one.
        
        Strategy:
        1. Try each possible number of shifts (0 to n-1)
        2. For each shift, create rotated string
        3. Check if it matches goal
        
        This is less efficient but more intuitive.
        Good to mention in interview before the optimal solution.
        """
        if len(s) != len(goal):
            return False
        
        if not s:
            return True
        
        # Try all possible rotations
        for i in range(len(s)):
            # Rotate by i positions: s[i:] + s[:i]
            rotated = s[i:] + s[:i]
            if rotated == goal:
                return True
        
        return False


