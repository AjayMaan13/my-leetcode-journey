"""
COUNT NUMBER OF SUBSTRINGS WITH EXACTLY K DISTINCT CHARACTERS

Problem Statement:
You are given a string s and a positive integer k. Return the number of 
substrings that contain exactly k distinct characters.

Example 1:
Input: s = "pqpqs", k = 2
Output: 7
Explanation: All substrings with exactly 2 distinct characters:
"pq", "pqp", "pqpq", "qp", "qpq", "pqs", "qs"
Total = 7

Example 2:
Input: s = "abcbaa", k = 3
Output: 5
Explanation: All substrings with exactly 3 distinct characters:
"abc", "abcb", "abcba", "bcba", "cbaa"
Total = 5
"""

from collections import defaultdict


# ==============================================================================
# APPROACH 1: SLIDING WINDOW WITH HELPER (OPTIMAL)
# ==============================================================================
# Time Complexity: O(n) - two passes through string
# Space Complexity: O(k) - frequency map stores at most k characters

class Solution:
    def substrCount(self, s, k):
        """
        Count substrings with exactly k distinct characters.
        
        Key Insight: 
        exactly(k) = atMost(k) - atMost(k-1)
        
        Why this works:
        - atMost(k) counts substrings with ≤ k distinct chars
        - atMost(k-1) counts substrings with ≤ k-1 distinct chars
        - Subtracting gives substrings with exactly k distinct chars
        
        Example: s = "abc", k = 2
        - atMost(2): "a","b","c","ab","bc" = 5 substrings
        - atMost(1): "a","b","c" = 3 substrings
        - exactly(2): 5 - 3 = 2 → "ab","bc" ✓
        """
        
        def atMostK(s, k):
            """
            Count substrings with at most k distinct characters.
            
            Uses sliding window technique:
            1. Expand window by moving right pointer
            2. Track character frequencies
            3. If distinct chars > k, shrink window from left
            4. For each valid window, all substrings ending at right are valid
            
            Key formula: (right - left + 1) substrings end at position right
            """
            left = 0
            result = 0
            freq = defaultdict(int)  # Maps character → frequency
            distinct = 0  # Count of distinct characters in window
            
            # Expand window with right pointer
            for right in range(len(s)):
                # Add new character to window
                if freq[s[right]] == 0:
                    distinct += 1  # New distinct character
                
                freq[s[right]] += 1  # Increment frequency
                
                # Shrink window if we have too many distinct characters
                while distinct > k:
                    # Remove leftmost character
                    freq[s[left]] -= 1
                    
                    # If character frequency becomes 0, we lost a distinct char
                    if freq[s[left]] == 0:
                        distinct -= 1
                    
                    left += 1  # Move window left boundary
                
                # Count valid substrings ending at right
                # All substrings from left to right are valid
                # Example: window "abc" has 3 substrings: "c", "bc", "abc"
                result += right - left + 1
            
            return result
        
        # Calculate exactly k using the formula
        return atMostK(s, k) - atMostK(s, k - 1)


# ==============================================================================
# APPROACH 2: ALTERNATIVE WITH DICT.GET (FROM PROBLEM)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(k)

class Solution_DictGet:
    def substrCount(self, s, k):
        """
        Same algorithm but using dict.get() instead of defaultdict.
        """
        
        def at_most_k_distinct(s, k):
            """Count substrings with at most k distinct characters"""
            left = 0
            res = 0
            freq = {}  # Regular dict instead of defaultdict
            
            # Iterate with right pointer
            for right in range(len(s)):
                # Add character to window
                # Use get() with default 0 to handle missing keys
                freq[s[right]] = freq.get(s[right], 0) + 1
                
                # Shrink window if distinct characters exceed k
                # len(freq) gives count of distinct characters
                while len(freq) > k:
                    # Decrement frequency of leftmost character
                    freq[s[left]] -= 1
                    
                    # Remove character if frequency becomes 0
                    if freq[s[left]] == 0:
                        del freq[s[left]]
                    
                    left += 1  # Shrink window
                
                # Count substrings in current window
                # Every position from left to right contributes a substring
                res += (right - left + 1)
            
            return res
        
        # Apply the formula: exactly k = atMost k - atMost (k-1)
        return at_most_k_distinct(s, k) - at_most_k_distinct(s, k - 1)


# ==============================================================================
# APPROACH 3: BRUTE FORCE (FOR COMPARISON)
# ==============================================================================
# Time Complexity: O(n²)
# Space Complexity: O(k)

class Solution_BruteForce:
    def substrCount(self, s, k):
        """
        Brute force: Check every substring.
        
        Not optimal but helps understand the problem.
        """
        count = 0
        n = len(s)
        
        # Try every starting position
        for i in range(n):
            seen = set()  # Track distinct characters
            
            # Try every ending position from i
            for j in range(i, n):
                seen.add(s[j])
                
                # If we have exactly k distinct chars, count this substring
                if len(seen) == k:
                    count += 1
                
                # If we exceed k, no point continuing from this i
                elif len(seen) > k:
                    break
        
        return count
