"""
14. LONGEST COMMON PREFIX

Problem Statement:
Write a function to find the longest common prefix string amongst an array 
of strings. If there is no common prefix, return an empty string "".

Example 1:
Input: strs = ["flower","flow","flight"]
Output: "fl"

Example 2:
Input: strs = ["dog","racecar","car"]
Output: ""
Explanation: There is no common prefix among the input strings.

Constraints:
- 1 <= strs.length <= 200
- 0 <= strs[i].length <= 200
- strs[i] consists of only lowercase English letters
"""


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (VERTICAL SCANNING WITH FLAG)
# ==============================================================================
# Time Complexity: O(S) where S is sum of all characters in all strings
# Space Complexity: O(1)

class Solution_VerticalScanning:
    def longestCommonPrefix(self, strs):
        """
        Compare character by character vertically across all strings.
        Use a flag to track if mismatch found.
        
        Strategy:
        1. Find minimum length among all strings
        2. For each position i (0 to min_len):
           - Compare strs[0][i] with all other strings at position i
           - If mismatch found, set flag and break
        3. Track last matching index
        """
        if len(strs) < 1:
            return ""

        # Find shortest string length (prefix can't be longer than this)
        min_len = min(len(s) for s in strs)
        
        lastIndex = -1  # Track last matching position
        match = True    # Flag to track if current position matches
        i = 0
        
        # Check each character position
        while i < min_len and match:
            # Compare first string's character with all others
            for j in range(1, len(strs)):
                if strs[0][i] != strs[j][i]:
                    match = False  # Mismatch found
                    break
            
            # If all matched at this position, update lastIndex
            if match:
                lastIndex = i + 1
            i += 1
        
        # Return prefix up to last matching position
        return strs[0][0:lastIndex] if lastIndex > 0 else ""


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (CLEANER VERTICAL SCANNING)
# ==============================================================================
# Time Complexity: O(S)
# Space Complexity: O(1)
#
# Improvement: Cleaner logic, early return on mismatch

class Solution_VerticalScanningClean:
    def longestCommonPrefix(self, strs):
        """
        Cleaner version of vertical scanning with early return.
        
        Strategy:
        1. Find minimum length
        2. For each position, compare all strings
        3. Return immediately when mismatch found
        4. If loop completes, prefix is entire min_len substring
        
        This is cleaner because:
        - Early return instead of flag variable
        - More straightforward logic
        """
        if not strs:
            return ""

        # Find shortest string length
        min_len = min(len(s) for s in strs)
        first = strs[0]
        
        # Check each character position
        for i in range(min_len):
            # Compare with all other strings
            for s in strs[1:]:
                if s[i] != first[i]:
                    # Mismatch found - return prefix so far
                    return first[0:i]
        
        # All characters matched up to min_len
        return first[0:min_len]


# ==============================================================================
# APPROACH 3: YOUR THIRD SOLUTION (SORTING - CLEVER!)
# ==============================================================================
# Time Complexity: O(S + n log n) where S is sum of chars, n is array length
# Space Complexity: O(1) if sorting in place, O(n) for sort
#
# Key Insight: After sorting, only need to compare first and last strings!

class Solution:
    def longestCommonPrefix(self, strs):
        """
        Sort array and compare only first and last strings.
        
        Brilliant insight! After lexicographic sorting:
        - First string has lexicographically smallest prefix
        - Last string has lexicographically largest prefix
        - Common prefix of ALL strings = common prefix of first & last
        
        Why this works:
        - Sorting arranges strings by dictionary order
        - If first and last share prefix, all middle strings must too
        - Example: ["flight", "flow", "flower"]
          After sort: ["flight", "flow", "flower"]
          Compare first & last: "flight" vs "flower" → "fl"
        
        This is elegant but note:
        - Sorting has O(n log n) overhead
        - For small n, vertical scanning might be faster
        - For large n with short strings, this can be better
        """
        # Handle empty list
        if not strs:
            return ""
        
        # Sort lexicographically
        strs.sort()
        
        # First and last strings after sorting
        first = strs[0]
        last = strs[-1]
        
        # Store common prefix characters
        ans = []
        
        # Compare characters of first and last
        for i in range(min(len(first), len(last))):
            # Stop if characters differ
            if first[i] != last[i]:
                return ''.join(ans)
            # Add matching character
            ans.append(first[i])
        
        # Return the longest common prefix
        return ''.join(ans)


# ==============================================================================
# APPROACH 4: HORIZONTAL SCANNING (ALTERNATIVE)
# ==============================================================================
# Time Complexity: O(S)
# Space Complexity: O(1)

class Solution_Horizontal:
    def longestCommonPrefix(self, strs):
        """
        Start with first string as prefix, reduce it with each string.
        
        Strategy:
        1. Start with prefix = strs[0]
        2. For each subsequent string, reduce prefix
        3. If prefix becomes empty, return ""
        
        This is intuitive but potentially less efficient if prefix
        gets reduced slowly.
        """
        if not strs:
            return ""
        
        prefix = strs[0]
        
        # Compare with each string
        for s in strs[1:]:
            # Reduce prefix while it doesn't match start of s
            while not s.startswith(prefix):
                prefix = prefix[:-1]  # Remove last character
                if not prefix:
                    return ""
        
        return prefix
