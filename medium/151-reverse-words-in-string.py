"""
151. REVERSE WORDS IN A STRING

Problem Statement:
Given an input string s, reverse the order of the words.

A word is defined as a sequence of non-space characters. The words in s will 
be separated by at least one space.

Return a string of the words in reverse order concatenated by a single space.

Note: s may contain leading or trailing spaces or multiple spaces between two 
words. The returned string should only have a single space separating the words.

Example 1:
Input: s = "the sky is blue"
Output: "blue is sky the"

Example 2:
Input: s = "  hello world  "
Output: "world hello"
Explanation: Your reversed string should not contain leading or trailing spaces.

Example 3:
Input: s = "a good   example"
Output: "example good a"
Explanation: You need to reduce multiple spaces between two words to a single 
space in the reversed string.
"""


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (STRING CONCATENATION)
# ==============================================================================
# Time Complexity: O(n) - single pass through string
# Space Complexity: O(n) - for result list and temp string

class Solution_StringConcat:
    def reverseWords(self, s):
        """
        Manually parse words using string concatenation.
        
        Strategy:
        1. Build words character by character using string concatenation
        2. Add complete words to result list
        3. Reverse the list and join with space
        
        Note: String concatenation in Python creates new string each time,
        so this is slightly less efficient than using a list of characters.
        """
        res = []
        temp = ""  # Build current word using string concatenation
        
        for ch in s:
            if ch != " ":
                temp += ch  # Add character to current word
            else:
                # Space encountered - word complete
                if temp:  # Only add non-empty words (handles multiple spaces)
                    res.append(temp)
                temp = ""  # Reset for next word
        
        # Don't forget last word (no trailing space)
        if temp:
            res.append(temp)
        
        # Reverse list and join with single space
        return " ".join(reversed(res))


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (LIST OF CHARACTERS - BETTER)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n)
#
# Improvement: Use list for building words instead of string concatenation

class Solution_ListChars:
    def reverseWords(self, s):
        """
        Manually parse words using list of characters (more efficient).
        
        Strategy:
        1. Build words character by character using list append (O(1))
        2. Join characters to form word when complete
        3. Reverse the words list and join with space
        
        This is more efficient than string concatenation because:
        - List append is O(1) vs string concatenation O(n)
        - Better for building strings character by character
        """
        res = []
        word = []  # Build current word using list of characters
        
        for ch in s:
            if ch != " ":
                word.append(ch)  # O(1) append operation
            else:
                # Space encountered - word complete
                if word:  # Only add non-empty words
                    res.append("".join(word))  # Join characters into word
                    word = []  # Reset for next word
        
        # Don't forget last word
        if word:
            res.append("".join(word))
        
        # Reverse list in place
        res.reverse()
        
        # Join with single space
        return " ".join(res)


# ==============================================================================
# APPROACH 3: BUILT-IN SPLIT (MOST PYTHONIC - BEST FOR INTERVIEWS)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n)
#
# Best approach for Python - clean, readable, handles all edge cases

class Solution:
    def reverseWords(self, s):
        """
        Use Python's built-in split() method - most elegant solution.
        
        Key insight: split() without arguments automatically:
        - Splits on any whitespace (space, tab, newline, etc.)
        - Removes leading/trailing whitespace
        - Handles multiple consecutive spaces
        - Returns list of non-empty words
        
        This is the preferred solution in interviews for Python:
        - Clean and readable
        - Handles all edge cases automatically
        - Pythonic idiom
        """
        # Option 1: Split, reverse in place, join
        words = s.split()  # Automatically handles all whitespace
        words.reverse()    # Reverse in place
        return " ".join(words)
        
        # Option 2: Split and use slicing (one-liner)
        return " ".join(s.split()[::-1])


# ==============================================================================
# APPROACH 4: TWO-POINTER (FOLLOW-UP - IN-PLACE IF ALLOWED)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1) if we can modify input, O(n) for result
#
# If interviewer asks for "minimal space" or "in-place" solution

class Solution_TwoPointer:
    def reverseWords(self, s):
        """
        Two-pointer approach - useful if in-place modification is required.
        
        Strategy:
        1. Convert string to list (strings are immutable in Python)
        2. Reverse entire string
        3. Reverse each word individually
        4. Clean up extra spaces
        
        This demonstrates algorithmic thinking but is overkill for Python.
        Use only if interviewer specifically asks for in-place solution.
        """
        # Convert to list for in-place modification
        chars = list(s.strip())
        n = len(chars)
        
        # Helper function to reverse a portion of the list
        def reverse(left, right):
            while left < right:
                chars[left], chars[right] = chars[right], chars[left]
                left += 1
                right -= 1
        
        # Step 1: Reverse entire string
        reverse(0, n - 1)
        
        # Step 2: Reverse each word
        start = 0
        for end in range(n):
            if chars[end] == ' ':
                reverse(start, end - 1)
                start = end + 1
        # Reverse last word
        reverse(start, n - 1)
        
        # Step 3: Clean up spaces (remove multiple spaces)
        # This part gets complex, so for Python just use split/join
        return " ".join("".join(chars).split())

