"""
Finding Square Root of a Number using Binary Search
Difficulty: Easy-Medium

Problem Statement:
Given a positive integer n, find and return its square root.
If n is not a perfect square, return the floor value of sqrt(n).

Examples:
1. n = 36 → Output: 6 (sqrt(36) = 6.0)
2. n = 28 → Output: 5 (sqrt(28) ≈ 5.292, floor = 5)
3. n = 8 → Output: 2 (sqrt(8) ≈ 2.828, floor = 2)
"""

# ============================================================================
# SOLUTION 1: BRUTE FORCE - LINEAR SEARCH
# ============================================================================

class SolutionBruteForce:
    """
    Approach: Linear search from 1 to n
    
    Time Complexity: O(n)
    Space Complexity: O(1)
    
    Algorithm:
    - Loop from 1 to n
    - Check if i*i <= n
    - Keep updating answer until i*i > n
    """
    
    def floorSqrt(self, n):
        """
        :type n: int
        :rtype: int
        """
        ans = 0
        
        for i in range(1, n + 1):
            if i * i <= n:
                ans = i
            else:
                break
        
        return ans


# ============================================================================
# SOLUTION 2: OPTIMAL - BINARY SEARCH (STANDARD)
# ============================================================================

class SolutionBinarySearch:
    """
    Approach: Binary search on answer space [1, n]
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Algorithm:
    - Search range: 1 to n
    - If mid*mid <= n: store mid, search right for larger value
    - If mid*mid > n: search left for smaller value
    """
    
    def mySqrt(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x < 2:
            return x
        
        left, right, ans = 1, x // 2, 0
        
        while left <= right:
            mid = (left + right) // 2
            
            if mid * mid <= x:
                ans = mid
                left = mid + 1
            else:
                right = mid - 1
        
        return ans
