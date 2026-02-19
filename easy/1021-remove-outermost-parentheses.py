"""
1021. REMOVE OUTERMOST PARENTHESES

Problem Statement:
A valid parentheses string is primitive if it is nonempty and cannot be split 
into two nonempty valid parentheses strings.

Given a valid parentheses string s, consider its primitive decomposition:
s = P1 + P2 + ... + Pk, where Pi are primitive valid parentheses strings.

Return s after removing the outermost parentheses of every primitive string 
in the primitive decomposition of s.

Example 1:
Input: s = "(()())(())"
Output: "()()()"
Explanation: Primitive decomposition is "(()())" + "(())".
After removing outer parentheses: "()()" + "()" = "()()()".

Example 2:
Input: s = "(()())(())(()(()))"
Output: "()()()()(())"
Explanation: Primitive decomposition is "(()())" + "(())" + "(()(()))".
After removing outer parentheses: "()()" + "()" + "()(())" = "()()()()(())".

Example 3:
Input: s = "()()"
Output: ""
Explanation: Primitive decomposition is "()" + "()".
After removing outer parentheses: "" + "" = "".
"""


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (TRACK PRIMITIVE BOUNDARIES)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - for result string

class Solution_TrackBoundaries:
    def removeOuterParentheses(self, s):
        """
        Track the start and end of each primitive substring, then extract
        the content without outer parentheses.
        
        Strategy:
        1. Count opening/closing parentheses to track balance
        2. When balance reaches 0, we've found a complete primitive
        3. Extract substring excluding first and last characters
        """
        res = ""
        length = len(s)
        lastOpen = False      # Flag to track if we're in a primitive
        lastOpenIndex = 0     # Starting index of current primitive
        parenOpen = 0         # Balance counter
        
        for i in range(length):
            if s[i] == "(":
                parenOpen += 1
                # Mark start of new primitive
                if not lastOpen:
                    lastOpenIndex = i
                    lastOpen = True
            else:  # s[i] == ")"
                parenOpen -= 1
            
            # When balance is 0, we've found complete primitive
            if parenOpen == 0 and i != 0:
                # Extract substring excluding outer parentheses
                # [lastOpenIndex + 1 : i] skips first '(' and last ')'
                res = res + s[lastOpenIndex + 1 : i]
                lastOpen = False
        
        return res


# ==============================================================================
# APPROACH 2: YOUR OPTIMIZED SOLUTION (DEPTH TRACKING)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - for result list
#
# Key Insight: Use depth/level to determine if parenthesis is "outer" or not.
# Outer parentheses are at depth 0→1 (opening) and 1→0 (closing).

class Solution:
    def removeOuterParentheses(self, s):
        """
        Track depth level and only include parentheses that are NOT outer.
        
        Strategy:
        1. Opening '(': If already inside (depth > 0), it's not outer - include it
        2. Closing ')': After decrement, if still inside (depth > 0), not outer - include it
        
        Depth levels:
        - depth = 0: Outside any primitive
        - depth = 1: At outer level of current primitive (skip these)
        - depth > 1: Inside primitive (keep these)
        """
        res = []
        depth = 0  # Current nesting depth
        
        for ch in s:
            if ch == "(":
                # Only add if already inside a primitive (depth > 0)
                if depth > 0:
                    res.append(ch)
                depth += 1  # Increase depth after checking
            
            else:  # ch == ")"
                depth -= 1  # Decrease depth before checking
                # Only add if still inside primitive (depth > 0)
                if depth > 0:
                    res.append(ch)
        
        return "".join(res)


# ==============================================================================
# APPROACH 3: ALTERNATIVE EXPLANATION (SAME AS APPROACH 2)
# ==============================================================================
# More explicit version with comments for clarity

class Solution_Verbose:
    def removeOuterParentheses(self, s):
        """
        Same algorithm as Approach 2 but with detailed comments.
        
        The key insight is understanding what makes a parenthesis "outer":
        - Opening '(' is outer if it starts a primitive (depth goes 0→1)
        - Closing ')' is outer if it ends a primitive (depth goes 1→0)
        - All other parentheses are inner and should be kept
        """
        result = []
        depth = 0
        
        for char in s:
            if char == "(":
                # This '(' is NOT outer if we're already inside (depth > 0)
                if depth > 0:
                    result.append(char)
                # Always increment depth for opening parenthesis
                depth += 1
            
            else:  # char == ")"
                # Always decrement depth for closing parenthesis
                depth -= 1
                # This ')' is NOT outer if we're still inside (depth > 0)
                if depth > 0:
                    result.append(char)
        
        return "".join(result)

