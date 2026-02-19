"""
74. SEARCH A 2D MATRIX

Problem Statement:
You are given an m x n integer matrix with the following properties:
- Each row is sorted in non-decreasing order.
- The first integer of each row is greater than the last integer of the previous row.

Given an integer target, return true if target is in matrix or false otherwise.
You must write a solution in O(log(m * n)) time complexity.

Example 1:
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true

Example 2:
Input: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
"""


# ==============================================================================
# APPROACH 1: My SOLUTION (TWO BINARY SEARCHES)
# ==============================================================================
# Time Complexity: O(log m + log n) = O(log(m*n))
# Space Complexity: O(1)

class Solution_TwoBinarySearches:
    def searchMatrix(self, matrix, target):
        """
        Two-step approach:
        1. Binary search to find the correct row
        2. Binary search within that row
        """
        
        def rowBinarySearch(row):
            """
            Binary search on a specific row to find target.
            
            Returns: True if target found, False otherwise
            """
            low, high = 0, len(matrix[row]) - 1
            
            while low <= high:
                mid = (high + low) // 2
                
                if matrix[row][mid] == target:
                    return True
                elif matrix[row][mid] > target:
                    high = mid - 1  # Target in left half
                else:
                    low = mid + 1   # Target in right half
            
            return False
        
        # Edge case: target larger than entire matrix
        low, high = 0, len(matrix) - 1
        lastIndex = len(matrix[0]) - 1
        
        if target > matrix[high][lastIndex]:
            return False
        
        # Binary search to find the correct row
        # Find first row where last element >= target
        while low < high:
            mid = (high + low) // 2
            
            if matrix[mid][lastIndex] >= target:
                # Target could be in this row or above
                high = mid
            else:
                # Target must be in rows below
                low = mid + 1
        
        # Now 'high' points to the row where target might be
        return rowBinarySearch(high)


# ==============================================================================
# APPROACH 2: TREAT AS 1D ARRAY (OPTIMAL FOR INTERVIEWS)
# ==============================================================================
# Time Complexity: O(log(m * n))
# Space Complexity: O(1)
#
# Key Insight: Since rows are sorted AND first element of each row > last of 
# previous row, we can treat the entire matrix as one sorted 1D array!

class Solution:
    def searchMatrix(self, matrix, target):
        """
        Treat the 2D matrix as a flattened 1D sorted array.
        
        Key Insight: Matrix [[1,3,5,7],[10,11,16,20],[23,30,34,60]]
        can be viewed as [1,3,5,7,10,11,16,20,23,30,34,60]
        
        Convert 1D index to 2D: 
        - row = index // cols
        - col = index % cols
        """
        if not matrix or not matrix[0]:
            return False
        
        m, n = len(matrix), len(matrix[0])
        
        # Treat matrix as array of length m*n
        left, right = 0, m * n - 1
        
        while left <= right:
            mid = (left + right) // 2
            
            # Convert 1D index to 2D coordinates
            row = mid // n  # Which row
            col = mid % n   # Which column in that row
            
            mid_value = matrix[row][col]
            
            if mid_value == target:
                return True
            elif mid_value < target:
                left = mid + 1  # Search right half
            else:
                right = mid - 1  # Search left half
        
        return False
