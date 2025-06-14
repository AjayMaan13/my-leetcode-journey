"""
2235. Add Two Integers
https://leetcode.com/problems/add-two-integers/

Difficulty: Easy
Topics: Math
Date Solved: 2024-01-15

Problem:
Given two integers num1 and num2, return the sum of the two integers.

Example 1:
Input: num1 = 12, num2 = 5
Output: 17
Explanation: num1 is 12, num2 is 5, and their sum is 12 + 5 = 17, so 17 is returned.

Example 2:
Input: num1 = -10, num2 = 4
Output: -6
Explanation: num1 + num2 = -6, so -6 is returned.

Constraints:
-100 <= num1, num2 <= 100
"""

class Solution:
    def sum(self, num1: int, num2: int) -> int:
        """
        Approach: Simple Addition
        - Just add the two numbers together
        - This is a warm-up problem to get familiar with LeetCode format
        
        Time: O(1) - constant time operation
        Space: O(1) - no extra space needed
        """
        return num1 + num2

# Test cases
if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1
    num1, num2 = 12, 5
    result = solution.sum(num1, num2)
    print(f"Input: num1 = {num1}, num2 = {num2}")
    print(f"Output: {result}")  # Expected: 17
    print(f"Explanation: {num1} + {num2} = {result}")
    print()
    
    # Test case 2
    num1, num2 = -10, 4
    result = solution.sum(num1, num2)
    print(f"Input: num1 = {num1}, num2 = {num2}")
    print(f"Output: {result}")  # Expected: -6
    print(f"Explanation: {num1} + {num2} = {result}")
    print()
    
    # Test case 3 - edge cases
    num1, num2 = 0, 0
    result = solution.sum(num1, num2)
    print(f"Edge case: num1 = {num1}, num2 = {num2}")
    print(f"Output: {result}")  # Expected: 0