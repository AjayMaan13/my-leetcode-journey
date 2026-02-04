"""
73. Set Matrix Zeroes
Medium

Given an m x n integer matrix matrix, if an element is 0, set its entire row 
and column to 0's.

You must do it in place.

Example 1:
Input: matrix = [[1,1,1],[1,0,1],[1,1,1]]
Output: [[1,0,1],[0,0,0],[1,0,1]]

Example 2:
Input: matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
Output: [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

Constraints:
- m == matrix.length
- n == matrix[0].length
- 1 <= m, n <= 200
- -2^31 <= matrix[i][j] <= 2^31 - 1

Follow up:
- A straightforward solution using O(mn) space is probably a bad idea.
- A simple improvement uses O(m + n) space, but still not the best solution.
- Could you devise a constant space solution?
"""


class Solution(object):
    def setZeroes_original(self, matrix):
        """
        ORIGINAL SOLUTION (First Approach)
        
        Approach: Store all zero positions, then set rows and columns
        
        Issues:
        1. Space: O(k) where k = number of zeros (could be O(m×n) worst case)
        2. Redundant work: If multiple zeros in same row, processes that row multiple times
        3. Time complexity: O(k × (m + n)) due to nested loops
        
        Time Complexity: O(k × (m + n)) where k = number of zeros
        Space Complexity: O(k)
        """
        xLength = len(matrix)
        yLength = len(matrix[0])
        zeroIndexList = []
        
        for x in range(xLength):
            for y in range(yLength):
                if matrix[x][y] == 0:
                    zeroIndexList.append([x, y])
        
        for index in zeroIndexList:
            x, y = index[0], index[1]
            
            # Top to bottom
            for i in range(xLength):
                matrix[i][y] = 0
            
            # Left to right
            for j in range(yLength):
                matrix[x][j] = 0
    
    def setZeroes_optimized_v1(self, matrix):
        """
        OPTIMIZED SOLUTION V1 (Improved Approach)
        
        Approach: Store which rows and columns need to be zeroed (not individual positions)
        
        Improvements over original:
        1. Space: O(m + n) instead of O(k)
        2. No redundant work: Each row/column processed exactly once
        3. Time complexity: O(m × n) - optimal
        
        Time Complexity: O(m × n)
        Space Complexity: O(m + n)
        """
        m = len(matrix)
        n = len(matrix[0])
        zero_rows = set()
        zero_cols = set()
        
        # Find all rows and columns that contain zeros
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)
        
        # Set identified rows to zero
        for row in zero_rows:
            for j in range(n):
                matrix[row][j] = 0
        
        # Set identified columns to zero
        for col in zero_cols:
            for i in range(m):
                matrix[i][col] = 0
    
    
    
    def setZeroes_pythonic_v1_1(self, matrix):
        """
        PYTHONIC SOLUTION (Concise & Readable)
        
        Most readable version using Python idioms
        Same O(m + n) space as optimized_v1, but more Pythonic
        
        Time Complexity: O(m × n)
        Space Complexity: O(m + n)
        """
        m, n = len(matrix), len(matrix[0])
        
        # Find zeros using set comprehension (scans once)
        zeros = {(i, j) for i in range(m) for j in range(n) if matrix[i][j] == 0}
        zero_rows = {i for i, j in zeros}
        zero_cols = {j for i, j in zeros}
        
        # Set rows to zero (can replace entire row)
        for row in zero_rows:
            matrix[row] = [0] * n
        
        # Set columns to zero
        for col in zero_cols:
            for i in range(m):
                matrix[i][col] = 0
    
    
    def setZeroes_optimized_v2(self, matrix):
        """
        MOST OPTIMIZED SOLUTION V2 (O(1) Space - Interview Level)
        
        Approach: Use first row and column as markers
        
        Key Insight:
        - Use matrix[i][0] to mark if row i should be zero
        - Use matrix[0][j] to mark if column j should be zero
        - Handle first row/column separately (they're used as markers)
        
        Algorithm:
        1. Check if first row and first column originally have zeros
        2. Use first row/col as markers for rest of matrix
        3. Set zeros based on markers
        4. Finally handle first row and column
        
        Time Complexity: O(m × n)
        Space Complexity: O(1) - only two boolean flags
        """
        m = len(matrix)
        n = len(matrix[0])
        
        # Flags to track if first row/column should be zero
        first_row_zero = False
        first_col_zero = False
        
        # Check if first row has zero
        for j in range(n):
            if matrix[0][j] == 0:
                first_row_zero = True
                break
        
        # Check if first column has zero
        for i in range(m):
            if matrix[i][0] == 0:
                first_col_zero = True
                break
        
        # Use first row and column as markers
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0  # Mark row
                    matrix[0][j] = 0  # Mark column
        
        # Set zeros based on markers (skip first row/col for now)
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        
        # Handle first row
        if first_row_zero:
            for j in range(n):
                matrix[0][j] = 0
        
        # Handle first column
        if first_col_zero:
            for i in range(m):
                matrix[i][0] = 0
                
    def setZeroes(self, matrix):
        """
        MOST OPTIMISED with LESS Only 1 Variable storage
        
        O(1) Space Solution - Uses first row/column as markers
        
        Do not return anything, modify matrix in-place instead.
        """
        ROWS, COLS = len(matrix), len(matrix[0])
        rowZero = False  # Flag to track if first row needs to be zeroed
        
        # Determine which rows/cols need to be zero
        # Use first row and first column as markers
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == 0:
                    matrix[0][c] = 0  # Mark column c using first row
                    
                    if r > 0:
                        matrix[r][0] = 0  # Mark row r using first column
                    else:
                        rowZero = True  # First row itself has a zero
        
        # Set zeros based on markers (skip first row and column for now)
        for r in range(1, ROWS):
            for c in range(1, COLS):
                # If row marker or column marker is 0, set cell to 0
                if matrix[0][c] == 0 or matrix[r][0] == 0:
                    matrix[r][c] = 0
        
        # Handle first column: if top-left cell is 0, zero out first column
        if matrix[0][0] == 0:
            for r in range(ROWS):
                matrix[r][0] = 0
        
        # Handle first row: if rowZero flag is set, zero out first row
        if rowZero:
            for c in range(COLS):
                matrix[0][c] = 0