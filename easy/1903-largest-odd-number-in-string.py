"""
1903. LARGEST ODD NUMBER IN STRING

Problem Statement:
You are given a string num, representing a large integer. Return the 
largest-valued odd integer (as a string) that is a non-empty substring of num, 
or an empty string "" if no odd integer exists.

A substring is a contiguous sequence of characters within a string.

Example 1:
Input: num = "52"
Output: "5"
Explanation: The only non-empty substrings are "5", "2", and "52". 
"5" is the only odd number.

Example 2:
Input: num = "4206"
Output: ""
Explanation: There are no odd numbers in "4206".

Example 3:
Input: num = "35427"
Output: "35427"
Explanation: "35427" is already an odd number.

Constraints:
- 1 <= num.length <= 10^5
- num only consists of digits
"""


# ==============================================================================
# APPROACH 1: MY SOLUTION (ITERATE FROM RIGHT)
# ==============================================================================
# Time Complexity: O(n) - worst case scan entire string
# Space Complexity: O(1) - only storing index

class Solution_Iterate:
    def largestOddNumber(self, num):
        """
        Find rightmost odd digit and return substring from start to there.
        
        Key Insight: A number is odd if and only if its last digit is odd.
        To get the largest odd substring, we need the longest possible string
        that ends with an odd digit.
        
        Strategy:
        1. Iterate from right to left
        2. Find first odd digit
        3. Return substring from start to that position
        
        Why this works:
        - Any substring ending with odd digit is odd
        - Longer substring = larger number (all digits are non-negative)
        - So we want the longest substring ending in odd digit
        - That's from index 0 to rightmost odd digit
        """
        if not num:
            return ""
        
        # Scan from right to left
        for i in range(len(num) - 1, -1, -1):
            # Check if current digit is odd
            if int(num[i]) % 2 != 0:
                # Return from start to this odd digit (inclusive)
                return num[0 : i + 1]
        
        # No odd digit found
        return ""


# ==============================================================================
# APPROACH 2: ALTERNATIVE CHECK (STRING SET MEMBERSHIP)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# Same logic but uses string membership instead of modulo

class Solution_SetCheck:
    def largestOddNumber(self, num):
        """
        Same algorithm but check odd using string membership.
        
        Slightly faster than int conversion + modulo since:
        - No type conversion needed
        - Direct character comparison
        - Set lookup is O(1)
        """
        if not num:
            return ""
        
        # Odd digits
        odd_digits = {'1', '3', '5', '7', '9'}
        
        # Scan from right to left
        for i in range(len(num) - 1, -1, -1):
            if num[i] in odd_digits:
                return num[:i + 1]
        
        return ""


# ==============================================================================
# APPROACH 3: ONE-LINER WITH rstrip() (PYTHONIC)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# Most elegant solution using Python string method

class Solution:
    def largestOddNumber(self, num):
        """
        Strip all trailing even digits from the right.
        
        Brilliant one-liner solution!
        
        Key Insight: rstrip(chars) removes all trailing characters that
        are in the given set of chars.
        
        By stripping "02468" (all even digits), we're left with either:
        - A string ending in odd digit (the answer!)
        - Empty string (no odd digits exist)
        
        This is exactly what we need!
        """
        return num.rstrip("02468")


# ==============================================================================
# APPROACH 4: ALTERNATIVE ONE-LINER (SIMILAR IDEA)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_Alternative:
    def largestOddNumber(self, num):
        """
        Alternative one-liner using while loop (less Pythonic).
        
        Same idea but less elegant than rstrip().
        """
        # Strip even digits from right
        while num and int(num[-1]) % 2 == 0:
            num = num[:-1]
        return num
