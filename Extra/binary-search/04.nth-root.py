"""
Nth Root of a Number using Binary Search
Difficulty: Medium

Problem Statement:
Given two numbers N and M, find the Nth root of M.
The nth root of a number M is defined as a number X when raised to power N equals M.
If the nth root is not an integer, return -1.

Examples:
1. N = 3, M = 27 → Output: 3 (3³ = 27)
2. N = 4, M = 69 → Output: -1 (4th root of 69 is not an integer)
3. N = 2, M = 16 → Output: 4 (4² = 16)
4. N = 5, M = 32 → Output: 2 (2⁵ = 32)
"""

# ============================================================================
# SOLUTION 1: BRUTE FORCE - LINEAR SEARCH
# ============================================================================

class SolutionBruteForce:
    """
    Approach: Linear search from 1 to M
    
    Time Complexity: O(M * N) - M iterations, each computing N-th power
    Space Complexity: O(1)
    
    Algorithm:
    - Try every number from 1 to M
    - Compute i^N for each number
    - Return i if i^N == M
    - Break if i^N > M (no point continuing)
    """
    
    def nthRoot(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """
        for i in range(1, m + 1):
            power = i ** n
            
            if power == m:
                return i
            
            if power > m:
                break
        
        return -1


# ============================================================================
# SOLUTION 2: OPTIMAL - BINARY SEARCH (STANDARD)
# ============================================================================

class SolutionBinarySearch:
    """
    Approach: Binary search with manual power calculation
    
    Time Complexity: O(log M * N) - log M iterations, each computing N-th power
    Space Complexity: O(1)
    
    Algorithm:
    - Search range: 1 to M
    - For each mid, compute mid^N manually (to detect overflow early)
    - If mid^N == M: found answer
    - If mid^N < M: search right half
    - If mid^N > M: search left half
    """
    
    def nthRoot(self, n, m):
        """
        :type n: int
        :type m: int
        :rtype: int
        """
        low, high = 1, m
        
        while low <= high:
            mid = (low + high) // 2
            
            ans = 1
            for _ in range(n):
                ans *= mid
                if ans > m:
                    break
            
            if ans == m:
                return mid
            
            if ans < m:
                low = mid + 1
            else:
                high = mid - 1
        
        return -1
