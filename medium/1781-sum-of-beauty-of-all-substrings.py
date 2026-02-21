"""
1781. SUM OF BEAUTY OF ALL SUBSTRINGS

Problem Statement:
The beauty of a string is the difference in frequencies between the most 
frequent and least frequent characters.

For example, the beauty of "abaacc" is 3 - 1 = 2.

Given a string s, return the sum of beauty of all of its substrings.

Example 1:
Input: s = "aabcb"
Output: 5
Explanation: The substrings with non-zero beauty are:
["aab","aabc","aabcb","abcb","bcb"], each with beauty = 1.

Example 2:
Input: s = "aabcbaa"
Output: 17
"""

from collections import Counter


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (NESTED LOOPS WITH HELPER)
# ==============================================================================
# Time Complexity: O(n³) - two loops + recounting for each substring
# Space Complexity: O(n) - for substring slicing and frequency map

class Solution_Nested:
    def beautySum(self, s):
        """
        Generate all substrings and calculate beauty for each.
        
        Strategy:
        1. Try all possible substrings [i, j]
        2. For each substring, count character frequencies
        3. Find max and min frequencies to get beauty
        4. Sum all beauties
        
        Problem: Recounting frequencies for each substring is inefficient.
        - O(n²) substrings
        - O(n) to count each substring
        - Total: O(n³)
        
        This works but is not optimal.
        """
        if not s:
            return 0
        
        def beauty(l, r):
            """
            Calculate beauty of substring s[l:r].
            
            Beauty = max_frequency - min_frequency
            """
            maxFreq = 0
            freqMap = {}
            
            # Count frequencies in substring
            for ch in s[l:r]:
                freqMap[ch] = 1 + freqMap.get(ch, 0)
                if freqMap[ch] > maxFreq:
                    maxFreq = freqMap[ch]
            
            # Find minimum frequency (greater than 0)
            minFreq = maxFreq
            for ch, freq in freqMap.items():
                if freq < minFreq and freq > 0:
                    minFreq = freq
            
            return maxFreq - minFreq
        
        beautySum = 0
        
        # Try all possible substrings
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                # Calculate beauty for substring s[i:j+1]
                beautySum += beauty(i, j + 1)
        
        return beautySum


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (INCREMENTAL FREQUENCY - OPTIMAL)
# ==============================================================================
# Time Complexity: O(n² * k) where k = 26 (alphabet size) → O(n²)
# Space Complexity: O(k) → O(1)
#
# This is the OPTIMAL solution!

class Solution:
    def beautySum(self, s):
        """
        Incrementally build frequency map as we extend substring.
        
        Key Optimization: Instead of recounting for each substring,
        maintain and update frequency map as we extend the right boundary.
        
        Strategy:
        1. For each starting position i:
           - Initialize empty frequency map
           - Extend right boundary j from i to end
           - Update frequency incrementally as we add s[j]
           - Calculate beauty without recounting
        
        Improvement:
        - No substring slicing
        - No recounting for each substring
        - Update frequency in O(1), find min/max in O(26) = O(1)
        - Total: O(n²)
        
        This is the RECOMMENDED solution!
        """
        if not s:
            return 0
        
        beautySum = 0
        
        # Try each starting position
        for i in range(len(s)):
            # Frequency map for current window
            freqMap = {}  # OR freq = [0] * 26 for array approach
            maxFreq = 0
            
            # Extend right boundary
            for j in range(i, len(s)):
                # Add current character to frequency map
                freqMap[s[j]] = 1 + freqMap.get(s[j], 0)
                
                # Update max frequency
                maxFreq = max(freqMap[s[j]], maxFreq)
                
                # Find min frequency among all characters in current substring
                minFreq = float('inf')
                for ch, freq in freqMap.items():
                    minFreq = min(minFreq, freq)
                
                # Add beauty of current substring to sum
                beautySum += maxFreq - minFreq
        
        return beautySum

# ==============================================================================
# APPROACH 3: OPTIMIZED MIN TRACKING (EVEN BETTER)
# ==============================================================================
# Time Complexity: O(n²)
# Space Complexity: O(1)

class Solution_OptimizedMin:
    def beautySum(self, s):
        """
        Track min more efficiently by only checking updated character.
        
        Further optimization: When we increment freq[s[j]], we know:
        - maxFreq might increase (check new freq vs current max)
        - minFreq needs recalculation (must scan all non-zero)
        
        This is as good as it gets without more complex data structures.
        """
        if not s:
            return 0
        
        beautySum = 0
        
        for i in range(len(s)):
            freq = [0] * 26
            maxFreq = 0
            
            for j in range(i, len(s)):
                # Update frequency
                idx = ord(s[j]) - ord('a')
                freq[idx] += 1
                
                # Update max frequency
                maxFreq = max(maxFreq, freq[idx])
                
                # Find min frequency (only among non-zero frequencies)
                minFreq = float('inf')
                
                for f in freq:
                    if f > 0:
                        minFreq = min(minFreq, f)
                # OR
                # minFreq = min(f for f in freq if f > 0)
                
                # Add beauty
                beautySum += maxFreq - minFreq
        
        return beautySum

