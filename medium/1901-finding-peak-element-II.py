"""
1901. FIND A PEAK ELEMENT II

Problem Statement:
A peak element in a 2D grid is an element that is strictly greater than all 
of its adjacent neighbors to the left, right, top, and bottom.

Given a 0-indexed m x n matrix mat where no two adjacent cells are equal, 
find any peak element mat[i][j] and return the length 2 array [i,j].

You may assume that the entire matrix is surrounded by an outer perimeter 
with the value -1 in each cell.

You must write an algorithm that runs in O(m log(n)) or O(n log(m)) time.

Example 1:
Input: mat = [[1,4],[3,2]]
Output: [0,1]
Explanation: Both 3 and 4 are peak elements so [1,0] and [0,1] are acceptable.

Example 2:
Input: mat = [[10,20,15],[21,30,14],[7,16,32]]
Output: [1,1]
Explanation: Both 30 and 32 are peak elements so [1,1] and [2,2] are acceptable.
"""


# ==============================================================================
# APPROACH: BINARY SEARCH ON COLUMNS + FIND MAX IN COLUMN
# ==============================================================================
# Time Complexity: O(m * log n) - log n binary search iterations, O(m) per iteration
# Space Complexity: O(1)
#
# Key Insight: Binary search on columns. For each middle column, find the row
# with max value. If that element is not a peak, move towards the larger neighbor.
# A peak is guaranteed to exist in that direction.

class Solution:
    def findPeakGrid(self, mat):
        """
        Find a peak element in 2D matrix using binary search on columns.
        
        Strategy:
        1. Binary search on columns (left to right)
        2. For each middle column, find the maximum element (scan all rows)
        3. Check if this max element is a peak by comparing with left/right neighbors
        4. If not a peak, move towards the larger neighbor
        5. A peak is guaranteed in that direction
        
        Why this works:
        - The maximum element in a column is guaranteed to be larger than
          its top/bottom neighbors (since it's the max in that column)
        - We only need to check left and right neighbors
        - Moving toward larger neighbor guarantees we'll find a peak
        """
        rows = len(mat)
        cols = len(mat[0])

        left = 0
        right = cols - 1

        # Binary search on columns
        while left <= right:
            # Pick middle column
            mid_col = (left + right) // 2

            # Step 1: Find the row with maximum value in this middle column
            # This element is guaranteed to be larger than its top/bottom neighbors
            max_row = 0
            for r in range(rows):
                if mat[r][mid_col] > mat[max_row][mid_col]:
                    max_row = r

            # Current cell is our candidate peak
            current = mat[max_row][mid_col]

            # Step 2: Get left and right neighbor values safely
            # Use -infinity for out-of-bounds (matrix surrounded by -1 conceptually)
            left_val = mat[max_row][mid_col - 1] if mid_col - 1 >= 0 else float('-inf')
            right_val = mat[max_row][mid_col + 1] if mid_col + 1 < cols else float('-inf')

            # Step 3: Check if current element is a peak
            # A peak must be greater than ALL neighbors (left, right, top, bottom)
            # Since current is max in column, it's already > top and bottom
            # We only need to check left and right
            if current > left_val and current > right_val:
                # Found a peak! Return its coordinates
                return [max_row, mid_col]

            # Step 4: Move towards the larger neighbor
            # Peak is guaranteed to exist in the direction of larger value
            elif right_val > current:
                # Right neighbor is larger, peak must be on right side
                # Eliminate left half including mid_col
                left = mid_col + 1
            else:
                # Left neighbor is larger (or equal, but problem says no equal neighbors)
                # Peak must be on left side
                # Eliminate right half including mid_col
                right = mid_col - 1

        # Should never reach here if input is valid
        return [-1, -1]


# ==============================================================================
# ALTERNATIVE: BINARY SEARCH ON ROWS (SAME COMPLEXITY)
# ==============================================================================
# Time Complexity: O(n * log m) - log m binary search iterations, O(n) per iteration
# Space Complexity: O(1)

class Solution_SearchRows:
    def findPeakGrid(self, mat):
        """
        Same algorithm but binary search on rows instead of columns.
        Results in O(n * log m) instead of O(m * log n).
        """
        rows = len(mat)
        cols = len(mat[0])

        top = 0
        bottom = rows - 1

        # Binary search on rows
        while top <= bottom:
            # Pick middle row
            mid_row = (top + bottom) // 2

            # Find column with maximum value in this middle row
            max_col = 0
            for c in range(cols):
                if mat[mid_row][c] > mat[mid_row][max_col]:
                    max_col = c

            # Current cell is candidate peak
            current = mat[mid_row][max_col]

            # Get top and bottom neighbor values
            top_val = mat[mid_row - 1][max_col] if mid_row - 1 >= 0 else float('-inf')
            bottom_val = mat[mid_row + 1][max_col] if mid_row + 1 < rows else float('-inf')

            # Check if current is a peak
            if current > top_val and current > bottom_val:
                return [mid_row, max_col]

            # Move towards larger neighbor
            elif bottom_val > current:
                # Peak must be below
                top = mid_row + 1
            else:
                # Peak must be above
                bottom = mid_row - 1

        return [-1, -1]

