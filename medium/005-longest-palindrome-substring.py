"""
5. LONGEST PALINDROMIC SUBSTRING

Problem Statement:
Given a string s, return the longest palindromic substring in s.

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"

Constraints:
- 1 <= s.length <= 1000
- s consist of only digits and English letters
"""


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (NESTED LOOPS - TLE)
# ==============================================================================
# Time Complexity: O(n³) - nested loops + palindrome check
# Space Complexity: O(1)
#
# This gets Time Limit Exceeded due to inefficiency

class Solution_Nested:
    def longestPalindrome(self, s):
        """
        Try all possible substrings and check if palindrome.
        
        Strategy:
        1. For each position, try expanding in both directions
        2. Use isPalindrome() to verify each substring
        3. Track longest palindrome found
        
        Problem: Redundant palindrome checks make this O(n³)
        - Outer loop: O(n)
        - Inner loop: O(n)
        - isPalindrome: O(n)
        
        This will TLE (Time Limit Exceeded) on large inputs.
        """
        if not s:
            return ""
        
        def isPalindrome(left, right):
            """Check if substring s[left:right+1] is palindrome"""
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True
        
        maxPalin = ""
        maxPalinLength = 0
        
        # Try each starting position
        for i in range(len(s)):
            l = r = i
            switch = False
            
            # Expand window
            while l > -1 and r < len(s):
                # Check if current window is palindrome
                if isPalindrome(l, r):
                    if maxPalinLength < (r - l + 1):
                        maxPalinLength = r - l + 1
                        maxPalin = s[l:r + 1]
                
                # Alternate between expanding left and right
                if switch:
                    l -= 1
                    switch = False
                else:
                    r += 1
                    switch = True
        
        return maxPalin


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (EXPAND AROUND CENTER - BETTER)
# ==============================================================================
# Time Complexity: O(n²) - for each center, expand O(n)
# Space Complexity: O(1)
#
# This is much better but still passes maxLength unnecessarily

class Solution_ExpandWithMaxLength:
    def longestPalindrome(self, s):
        """
        Expand around each possible center to find palindromes.
        
        Key Insight: Every palindrome has a center.
        - Odd length: center is a single character (e.g., "aba")
        - Even length: center is between two characters (e.g., "abba")
        
        Strategy:
        1. For each position, try both odd and even centers
        2. Expand while characters match
        3. Track the longest palindrome found
        
        Improvement over Approach 1:
        - No redundant palindrome checks
        - Expand only while characters match
        - O(n²) instead of O(n³)
        """
        if not s:
            return ""
        
        def expand(l, r, maxLength):
            """
            Expand around center and return length of palindrome.
            
            Note: Passing maxLength here is unnecessary overhead.
            """
            # Expand while characters match and within bounds
            while l > -1 and r < len(s) and s[l] == s[r]:
                if r - l + 1 > maxLength:
                    maxLength = r - l + 1
                l -= 1
                r += 1
            
            return maxLength
        
        start = 0       # Starting index of longest palindrome
        maxLength = 0   # Length of longest palindrome
        
        # Try each position as potential center
        for i in range(len(s)):
            # Check odd-length palindromes (center is s[i])
            len1 = expand(i, i, maxLength)
            
            # Check even-length palindromes (center is between s[i] and s[i+1])
            len2 = expand(i, i + 1, maxLength)
            
            # Take the longer palindrome
            length = max(len1, len2)
            
            # Update if we found a longer palindrome
            if length > maxLength:
                maxLength = length
                # Calculate starting position of palindrome
                # Formula: center - (length - 1) // 2
                start = i - (length - 1) // 2
        
        return s[start:start + maxLength]


# ==============================================================================
# APPROACH 3: EXPAND AROUND CENTER (OPTIMAL - CLEANEST)
# ==============================================================================
# Time Complexity: O(n²)
# Space Complexity: O(1)
#
# This is the BEST solution for interviews!

class Solution:
    def longestPalindrome(self, s):
        """
        Expand around center - cleanest implementation.
        
        Strategy:
        1. For each position, expand around it as center
        2. Try both odd-length and even-length palindromes
        3. Return the longest found
        
        Why this is better than Approach 2:
        - Cleaner expand function (no unnecessary maxLength parameter)
        - Same time complexity but simpler logic
        - Easy to explain in interviews
        
        This is the RECOMMENDED solution!
        """
        if not s:
            return ""
        
        def expand(l, r):
            """
            Expand around center while characters match.
            
            Returns: Length of palindrome found
            
            Key: Expand WHILE characters match, then calculate length.
            After loop, l and r are one step past the palindrome boundary.
            So length = (r-1) - (l+1) + 1 = r - l - 1
            """
            # Expand while within bounds and characters match
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            
            # l and r are now one position beyond the palindrome
            # Actual palindrome is s[l+1:r], length = r - l - 1
            return r - l - 1
        
        start = 0       # Starting index of longest palindrome
        maxLength = 0   # Length of longest palindrome
        
        # Try each position as center
        for i in range(len(s)):
            # Odd-length palindromes: single character center
            len1 = expand(i, i)
            
            # Even-length palindromes: center between two characters
            len2 = expand(i, i + 1)
            
            # Get the longer of the two
            length = max(len1, len2)
            
            # Update if this is the longest palindrome so far
            if length > maxLength:
                maxLength = length
                # Calculate starting index: i - (length - 1) // 2
                # For odd: center is i, start = i - length // 2
                # For even: center is between i and i+1, formula still works
                start = i - (length - 1) // 2
        
        return s[start:start + maxLength]


# ==============================================================================
# APPROACH 4: DYNAMIC PROGRAMMING (ALTERNATIVE O(n²))
# ==============================================================================
# Time Complexity: O(n²)
# Space Complexity: O(n²) - for DP table

class Solution_DP:
    def longestPalindrome(self, s):
        """
        Dynamic Programming approach.
        
        Strategy:
        1. dp[i][j] = True if s[i:j+1] is a palindrome
        2. Base case: single characters are palindromes
        3. Recurrence: s[i:j+1] is palindrome if:
           - s[i] == s[j] AND
           - s[i+1:j] is palindrome (or j - i <= 2)
        
        This works but uses O(n²) space, less optimal than expand approach.
        """
        n = len(s)
        if n == 0:
            return ""
        
        # DP table: dp[i][j] = is s[i:j+1] a palindrome?
        dp = [[False] * n for _ in range(n)]
        
        start = 0       # Start of longest palindrome
        maxLength = 1   # Length of longest palindrome
        
        # Every single character is a palindrome
        for i in range(n):
            dp[i][i] = True
        
        # Check for two-character palindromes
        for i in range(n - 1):
            if s[i] == s[i + 1]:
                dp[i][i + 1] = True
                start = i
                maxLength = 2
        
        # Check for palindromes of length 3 and above
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1  # Ending index
                
                # Check if s[i:j+1] is palindrome
                if s[i] == s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    start = i
                    maxLength = length
        
        return s[start:start + maxLength]

