"""
MEDIAN OF ROW WISE SORTED MATRIX

Problem Statement:
Given a row-wise sorted matrix of size M*N, where M is no. of rows and N is 
no. of columns, find the median in the given matrix.

Note: M*N is always odd.

Example 1:
Input: M = 3, N = 3, matrix = [[1,4,9],[2,5,6],[3,8,7]]
Output: 5
Explanation: Sorted array = [1,2,3,4,5,6,7,8,9], median = 5

Example 2:
Input: M = 3, N = 3, matrix = [[1,3,8],[2,3,4],[1,2,5]]
Output: 3
Explanation: Sorted array = [1,1,2,2,3,3,4,5,8], median = 3
"""

import bisect


# ==============================================================================
# APPROACH 1: BRUTE FORCE (FLATTEN AND SORT)
# ==============================================================================
# Time Complexity: O(M*N * log(M*N)) - sorting all elements
# Space Complexity: O(M*N) - storing all elements in a list

class Solution_BruteForce:
    def findMedian(self, matrix):
        """
        Flatten matrix into list, sort it, and return middle element.
        
        Strategy: 
        1. Collect all elements from matrix into a list
        2. Sort the list
        3. Return middle element (since M*N is odd)
        
        Simple but inefficient - doesn't use row-sorted property.
        """
        # Create a list to store all elements
        elements = []

        # Traverse each row
        for row in matrix:
            # Traverse each value in the row
            for val in row:
                # Add value to list
                elements.append(val)

        # Sort all collected elements
        elements.sort()

        # Return the middle value (median)
        # Since M*N is odd, median is at index (M*N) // 2
        return elements[len(elements) // 2]


# ==============================================================================
# APPROACH 2: BINARY SEARCH ON VALUE SPACE (OPTIMAL)
# ==============================================================================
# Time Complexity: O(M * log N * log(max - min))
# Space Complexity: O(1)
#
# Key Insight: Binary search on the answer (value range) instead of position.
# For each candidate value, count how many elements are ≤ it.
# The median is the smallest value with at least (M*N+1)/2 elements ≤ it.

class Solution:
    def countLessEqual(self, row, mid):
        """
        Count how many elements in a sorted row are ≤ mid.
        
        Uses binary search (bisect_right) to find position efficiently.
        bisect_right returns index where mid should be inserted to keep sorted order.
        This index equals the count of elements ≤ mid.
        
        Args:
            row: A sorted row from the matrix
            mid: Value to compare against
            
        Returns:
            Count of elements ≤ mid in this row
        """
        # bisect_right finds rightmost position to insert mid
        # This equals count of elements ≤ mid
        return bisect.bisect_right(row, mid)

    def findMedian(self, matrix):
        """
        Find median using binary search on value space.
        
        Strategy:
        1. Binary search between min and max values in matrix
        2. For each mid value, count how many elements ≤ mid
        3. If count < required median position, search higher values
        4. Otherwise, search lower values
        5. Converge to the median value
        
        Why this works:
        - Median is at position (M*N + 1) / 2 in sorted array
        - We binary search for smallest value with ≥ (M*N+1)/2 elements ≤ it
        - That value is the median!
        """
        rows = len(matrix)
        cols = len(matrix[0])

        # Define search space: [smallest element, largest element]
        # Smallest element is in first column (rows are sorted)
        low = min(row[0] for row in matrix)
        # Largest element is in last column
        high = max(row[-1] for row in matrix)

        # Required position of median in sorted array (1-indexed)
        # For odd M*N, median is at position (M*N + 1) / 2
        required = (rows * cols + 1) // 2

        # Binary search on value space
        while low < high:
            # Try mid as potential median value
            mid = (low + high) // 2
            count = 0

            # Count total elements ≤ mid across all rows
            for row in matrix:
                count += self.countLessEqual(row, mid)

            # Check if we have enough elements ≤ mid
            if count < required:
                # Not enough elements ≤ mid, median must be larger
                # Search in higher values
                low = mid + 1
            else:
                # We have enough elements ≤ mid
                # But median could be smaller, so search lower values
                high = mid

        # When low == high, we've found the median value
        return low


# ==============================================================================
# APPROACH 3: MANUAL BINARY SEARCH (WITHOUT BISECT)
# ==============================================================================
# Same complexity as optimal, but implements binary search manually

class Solution_Manual:
    def upperBound(self, arr, target):
        """
        Manually implement upper bound (bisect_right equivalent).
        
        Finds the rightmost position where target can be inserted.
        This equals count of elements ≤ target.
        """
        low, high = 0, len(arr)
        
        while low < high:
            mid = (low + high) // 2
            
            if arr[mid] <= target:
                # Current element ≤ target, search right
                low = mid + 1
            else:
                # Current element > target, search left
                high = mid
        
        return low  # Count of elements ≤ target

    def findMedian(self, matrix):
        """
        Same algorithm as optimal but with manual binary search.
        """
        rows = len(matrix)
        cols = len(matrix[0])

        # Find min and max in matrix
        low = min(row[0] for row in matrix)
        high = max(row[-1] for row in matrix)

        # Required median position
        required = (rows * cols + 1) // 2

        # Binary search on value space
        while low < high:
            mid = (low + high) // 2
            count = 0

            # Count elements ≤ mid using manual binary search
            for row in matrix:
                count += self.upperBound(row, mid)

            if count < required:
                low = mid + 1
            else:
                high = mid

        return low

