"""
240. SEARCH A 2D MATRIX II

Problem Statement:
Write an efficient algorithm that searches for a value target in an m x n 
integer matrix. This matrix has the following properties:
- Integers in each row are sorted in ascending from left to right.
- Integers in each column are sorted in ascending from top to bottom.

Note: Unlike problem 74, the first element of each row is NOT necessarily 
greater than the last element of the previous row.

Example 1:
Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],
                 [10,13,14,17,24],[18,21,23,26,30]], target = 5
Output: true

Example 2:
Input: matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],
                 [10,13,14,17,24],[18,21,23,26,30]], target = 20
Output: false
"""


# ==============================================================================
# APPROACH 1: My FIRST SOLUTION (BINARY SEARCH ON EACH ROW)
# ==============================================================================
# Time Complexity: O(m * log n) - binary search on each of m rows
# Space Complexity: O(1)

class Solution_BinarySearchEachRow:
    def searchMatrix(self, matrix, target):
        """
        Binary search on each row independently.
        
        Strategy: Since each row is sorted, perform binary search on every row.
        This works but doesn't utilize the column sorting property.
        """
        rows = len(matrix)
        columns = len(matrix[0])
        
        # Early termination: target larger than bottom-right element
        if target > matrix[rows - 1][columns - 1]:
            return False
        
        def searchOneSide(row):
            """
            Binary search on a specific row.
            
            Returns: True if target found, False otherwise
            """
            low = 0
            high = columns - 1  # Fixed: was 'columns', should be 'columns - 1'
            
            while low <= high:
                mid = (high + low) // 2
                
                if matrix[row][mid] == target:
                    return True
                elif matrix[row][mid] > target:
                    high = mid - 1  # Search left half
                else:
                    low = mid + 1   # Search right half
            
            return False
        
        # Search each row
        for i in range(rows):
            if searchOneSide(i):
                return True
        
        return False


# ==============================================================================
# APPROACH 2: STAIRCASE SEARCH (OPTIMAL)
# ==============================================================================
# Time Complexity: O(m + n) - visit at most m+n elements
# Space Complexity: O(1)
#
# Key Insight: Start from top-right (or bottom-left) corner. This position
# allows us to eliminate either a row or column with each comparison!

class Solution:
    def searchMatrix(self, matrix, target):
        """
        Staircase search starting from top-right corner.
        
        Why top-right?
        - Elements to the left are smaller (row is sorted)
        - Elements below are larger (column is sorted)
        - This gives us clear direction to move!
        
        At each step:
        - If current > target → move left (eliminate column)
        - If current < target → move down (eliminate row)
        - If current == target → found!
        """
        rows = len(matrix)
        cols = len(matrix[0])
        
        # Start from top-right corner
        r, c = 0, cols - 1
        
        # While we're within matrix bounds
        while r < rows and c >= 0:
            current = matrix[r][c]
            
            if current == target:
                return True  # Found target!
            
            elif current < target:
                # Current is too small, target must be below
                # Eliminate this row, move down
                r += 1
            
            else:  # current > target
                # Current is too large, target must be to the left
                # Eliminate this column, move left
                c -= 1
        
        # Exhausted search space without finding target
        return False


# ==============================================================================
# APPROACH 3: STAIRCASE FROM BOTTOM-LEFT (ALTERNATIVE)(MOST OPTIMAL)
# ==============================================================================
# Time Complexity: O(m + n)
# Space Complexity: O(1)
#
# Same algorithm but starting from bottom-left corner instead

class Solution_BottomLeft:
    def searchMatrix(self, matrix, target):
        """
        Staircase search starting from bottom-left corner.
        
        Why bottom-left?
        - Elements to the right are larger (row is sorted)
        - Elements above are smaller (column is sorted)
        - Also gives clear direction to move!
        
        At each step:
        - If current > target → move up (eliminate row)
        - If current < target → move right (eliminate column)
        - If current == target → found!
        """
        rows = len(matrix)
        cols = len(matrix[0])
        
        # Start from bottom-left corner
        r, c = rows - 1, 0
        
        while r >= 0 and c < cols:
            current = matrix[r][c]
            
            if current == target:
                return True
            
            elif current > target:
                # Current too large, move up
                r -= 1
            
            else:  # current < target
                # Current too small, move right
                c += 1
        
        return False


# ==============================================================================
# APPROACH 4: BINARY SEARCH ON DIAGONAL + RECURSION (ADVANCED)
# ==============================================================================
# Time Complexity: O(m * log n) or O(n * log m)
# Space Complexity: O(log(min(m, n))) - recursion stack
#
# More complex approach using divide and conquer

class Solution_DivideConquer:
    def searchMatrix(self, matrix, target):
        """
        Divide and conquer approach using binary search on diagonal.
        
        This is more complex than staircase but demonstrates advanced technique.
        Generally not recommended in interviews unless specifically asked.
        """
        if not matrix or not matrix[0]:
            return False
        
        def search(top, left, bottom, right):
            """
            Search in submatrix from (top, left) to (bottom, right)
            """
            # Base case: invalid submatrix
            if top > bottom or left > right:
                return False
            
            # If target is out of bounds of this submatrix
            if target < matrix[top][left] or target > matrix[bottom][right]:
                return False
            
            # Binary search on the diagonal
            mid_col = (left + right) // 2
            row = top
            
            # Find row on diagonal where we should split
            while row <= bottom and matrix[row][mid_col] <= target:
                if matrix[row][mid_col] == target:
                    return True
                row += 1
            
            # Search in top-right and bottom-left quadrants
            return (search(top, mid_col + 1, row - 1, right) or
                    search(row, left, bottom, mid_col - 1))
        
        return search(0, 0, len(matrix) - 1, len(matrix[0]) - 1)

