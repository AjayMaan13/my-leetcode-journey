"""
FIND THE ROW WITH MAXIMUM NUMBER OF 1's

Problem Statement:
You have been given a non-empty grid 'mat' with 'n' rows and 'm' columns 
consisting of only 0s and 1s. All the rows are sorted in ascending order.

Your task is to find the index of the row with the maximum number of ones.

Note: 
- If two rows have the same number of ones, consider the one with a smaller index.
- If there's no row with at least 1 zero, return -1.

Example 1:
Input: n = 3, m = 3, mat = [[1,1,1], [0,0,1], [0,0,0]]
Output: 0
Explanation: Row 0 has the maximum number of ones (3 ones).

Example 2:
Input: n = 2, m = 2, mat = [[0,0], [0,0]]
Output: -1
Explanation: No 1s in the matrix.
"""


# ==============================================================================
# APPROACH 1: BRUTE FORCE
# ==============================================================================
# Time Complexity: O(n * m) - traverse entire matrix
# Space Complexity: O(1)

class Solution_BruteForce:
    def row_with_max_1s(self, matrix, n, m):
        """
        Count 1s in each row by traversing all elements.
        
        Strategy: Go through every element in every row and count 1s.
        Keep track of which row has the most 1s.
        """
        cnt_max = 0  # Tracks maximum number of 1s found so far
        index = -1   # Stores row index with maximum 1s (-1 if no 1s found)

        # Traverse each row
        for i in range(n):
            cnt_ones = 0  # Count of 1s in current row
            
            # Count all 1s in this row
            for j in range(m):
                cnt_ones += matrix[i][j]  # Add 1 if element is 1, else add 0
            
            # Update if current row has more 1s than previous max
            if cnt_ones > cnt_max:
                cnt_max = cnt_ones
                index = i  # Update row index with most 1s

        # Return row index with most 1s (or -1 if no 1s found)
        return index


# ==============================================================================
# APPROACH 2: BINARY SEARCH (OPTIMAL)
# ==============================================================================
# Time Complexity: O(n * log m) - binary search on each row
# Space Complexity: O(1)
#
# Key Insight: Since each row is sorted, we can use binary search to find
# the first occurrence of 1. All elements after that are also 1s.

class Solution:
    def lower_bound(self, arr, n, x):
        """
        Find the first index where element >= x (lower bound).
        
        For a row like [0, 0, 0, 1, 1, 1], if x = 1, this returns index 3.
        This tells us where 1s start in the sorted row.
        
        Returns: Index of first element >= x, or n if not found
        """
        low, high = 0, n - 1
        ans = n  # Default: if x not found, return n (no 1s in row)

        # Binary search for first occurrence of element >= x
        while low <= high:
            mid = (low + high) // 2
            
            # If current element >= x, it could be our answer
            if arr[mid] >= x:
                ans = mid       # Store potential answer
                high = mid - 1  # Search left half for earlier occurrence
            else:
                # Current element < x, search right half
                low = mid + 1
        
        return ans  # Index where 1s start (or n if no 1s)

    def row_with_max_1s(self, matrix, n, m):
        """
        Find row with maximum 1s using binary search on each row.
        
        Optimization: Since rows are sorted, find where 1s start using
        binary search. Number of 1s = (total columns - start index).
        """
        cnt_max = 0   # Maximum number of 1s found so far
        index = -1    # Row index with maximum 1s

        # Check each row
        for i in range(n):
            # Find where 1s start in this row using binary search
            first_one_index = self.lower_bound(matrix[i], m, 1)
            
            # Calculate count of 1s in this row
            # If row is [0,0,0,1,1,1] and first_one_index = 3, then:
            # cnt_ones = 6 - 3 = 3 ones
            cnt_ones = m - first_one_index
            
            # Update if current row has more 1s
            if cnt_ones > cnt_max:
                cnt_max = cnt_ones
                index = i
        
        # Return row index with most 1s (or -1 if no 1s found)
        return index

