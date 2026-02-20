"""
1614. MAXIMUM NESTING DEPTH OF THE PARENTHESES

Problem Statement:
Given a valid parentheses string s, return the nesting depth of s.
The nesting depth is the maximum number of nested parentheses.

Example 1:
Input: s = "(1+(2*3)+((8)/4))+1"
Output: 3
Explanation: Digit 8 is inside of 3 nested parentheses in the string.

Example 2:
Input: s = "(1)+((2))+(((3)))"
Output: 3
Explanation: Digit 3 is inside of 3 nested parentheses in the string.

Example 3:
Input: s = "()(())((()()))"
Output: 3
"""


# ==============================================================================
# APPROACH 1: YOUR SOLUTION (SINGLE PASS WITH COUNTER - OPTIMAL)
# ==============================================================================
# Time Complexity: O(n) - single pass through string
# Space Complexity: O(1) - only using two variables

class Solution:
    def maxDepth(self, s):
        """
        Track current depth and update maximum as we scan the string.
        
        Key Insight: 
        - Opening '(' increases depth (going deeper)
        - Closing ')' decreases depth (coming back up)
        - Track maximum depth seen during the journey
        
        Strategy:
        1. Maintain currDepth counter (current nesting level)
        2. Maintain maxDepth (highest level reached)
        3. For '(': increment currDepth, update maxDepth
        4. For ')': decrement currDepth
        5. Ignore other characters (digits, operators)
        
        This is the OPTIMAL solution - O(n) time, O(1) space!
        """
        if not s:
            return 0
        
        maxDepth = 0    # Maximum depth encountered so far
        currDepth = 0   # Current depth/nesting level
        
        for ch in s:
            if ch == "(":
                # Going deeper into nesting
                currDepth += 1
                # Update max only when depth is increasing
                # This is the key optimization - we only update max here
                maxDepth = max(currDepth, maxDepth)
            
            elif ch == ")":
                # Coming back up from nesting
                currDepth -= 1
                # No need to check max here since we're decreasing
        
        return maxDepth



# ==============================================================================
# APPROACH 2: USING STACK (MORE VERBOSE)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - for stack

class Solution_Stack:
    def maxDepth(self, s):
        """
        Use explicit stack to track nesting.
        
        This is overkill for this problem but shows how stack relates
        to parentheses problems. Stack size at any point = current depth.
        
        Not recommended for this problem since we don't need the stack,
        but good to understand the connection.
        """
        if not s:
            return 0
        
        stack = []      # Stack to track open parentheses
        maxDepth = 0    # Maximum depth encountered
        
        for ch in s:
            if ch == "(":
                # Push onto stack (any value works, we only care about size)
                stack.append(ch)
                # Stack size = current depth
                maxDepth = max(maxDepth, len(stack))
            
            elif ch == ")":
                # Pop from stack
                if stack:  # Should always be true for valid input
                    stack.pop()
        
        return maxDepth

