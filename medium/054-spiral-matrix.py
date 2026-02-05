"""
54. Spiral Matrix
Medium

Given an m x n matrix, return all elements of the matrix in spiral order.

Example 1:
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]

Visualization:
[1, 2, 3]
[4, 5, 6]     →  Start at (0,0), go right → down → left → up → right...
[7, 8, 9]

Path: 1 → 2 → 3 → 6 → 9 → 8 → 7 → 4 → 5

Example 2:
Input: matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
Output: [1,2,3,4,8,12,11,10,9,5,6,7]

Visualization:
[1,  2,  3,  4]
[5,  6,  7,  8]    →  Spiral from outside to inside
[9, 10, 11, 12]

Path: 1 → 2 → 3 → 4 → 8 → 12 → 11 → 10 → 9 → 5 → 6 → 7

Constraints:
- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 10
- -100 <= matrix[i][j] <= 100
"""


class Solution(object):
    def spiralOrder_simulation(self, matrix):
        """
        APPROACH 1: Direction Simulation (My's Optimized Solution)
        
        Key Idea:
        - Track current position (row, column)
        - Track current direction (right, down, left, up)
        - Track boundaries (top, bottom, left, right)
        - When hitting boundary, change direction and update boundary
        
        Algorithm:
        1. Start at (0, 0) going right
        2. Add current element to result
        3. Try to move in current direction
        4. If hit boundary, change direction and update boundary
        5. Repeat until all elements added
        
        Time Complexity: O(m × n) - visit each element once
        Space Complexity: O(1) - excluding output array
        
        Pros:
        - Intuitive - simulates actual traversal
        - Easy to understand the movement
        - Single pass through matrix
        
        Cons:
        - More code with direction tracking
        - Multiple if-elif branches
        """
        if not matrix or not matrix[0]:
            return []
        
        output = [] 
        total_elements = len(matrix) * len(matrix[0])
        direction = "right"
        
        # Initialize boundaries
        left_boundary = top_boundary = 0
        right_boundary = len(matrix[0]) - 1
        bottom_boundary = len(matrix) - 1
        
        row, column = 0, 0
        
        while len(output) < total_elements:
            # Add current element
            output.append(matrix[row][column])
            
            # Move to next position based on current direction
            if direction == "right":
                if column < right_boundary:
                    column += 1
                else:
                    direction = "down"
                    top_boundary += 1
                    row += 1
                    
            elif direction == "down":
                if row < bottom_boundary:
                    row += 1
                else:
                    direction = "left"
                    right_boundary -= 1
                    column -= 1
                    
            elif direction == "left":
                if column > left_boundary:
                    column -= 1
                else:
                    direction = "top"
                    bottom_boundary -= 1
                    row -= 1
                    
            else:  # direction == "top"
                if row > top_boundary:
                    row -= 1
                else:
                    direction = "right"
                    left_boundary += 1
                    column += 1
        
        return output
    
    def spiralOrder_layer_by_layer(self, matrix):
        """
        APPROACH 2: Layer-by-Layer (Most Optimal & Clean)
        
        Key Idea:
        - Process matrix in layers from outside to inside
        - Each layer is a complete spiral: right → down → left → up
        - Shrink boundaries after each complete layer
        
        Algorithm:
        1. Define 4 boundaries: top, bottom, left, right
        2. While boundaries don't overlap:
           a. Go right across top row
           b. Go down along right column
           c. Go left across bottom row (if row exists)
           d. Go up along left column (if column exists)
        3. Shrink boundaries inward
        
        Example walkthrough for 3×4 matrix:
        [1,  2,  3,  4]
        [5,  6,  7,  8]
        [9, 10, 11, 12]
        
        Layer 1:
        - Right: 1, 2, 3, 4 (top row, columns 0-3)
        - Down:  8, 12 (right column, rows 1-2)
        - Left:  11, 10, 9 (bottom row, columns 2-0)
        - Up:    5 (left column, row 1)
        
        Layer 2:
        - Right: 6, 7 (top row, columns 1-2)
        - (no more elements)
        
        Time Complexity: O(m × n) - visit each element once
        Space Complexity: O(1) - excluding output array
        
        Pros:
        - Cleanest code
        - Most intuitive for spiral pattern
        - Easy to handle edge cases
        - Standard interview solution
        
        Cons:
        - Need to check if row/column still exists before left/up movements
        """
        if not matrix or not matrix[0]:
            return []
        
        result = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1
        
        while top <= bottom and left <= right:
            # Move right along top row
            for col in range(left, right + 1):
                result.append(matrix[top][col])
            top += 1
            
            # Move down along right column
            for row in range(top, bottom + 1):
                result.append(matrix[row][right])
            right -= 1
            
            # Move left along bottom row (if row still exists)
            if top <= bottom:
                for col in range(right, left - 1, -1):
                    result.append(matrix[bottom][col])
                bottom -= 1
            
            # Move up along left column (if column still exists)
            if left <= right:
                for row in range(bottom, top - 1, -1):
                    result.append(matrix[row][left])
                left += 1
        
        return result
    
    def spiralOrder(self, matrix):
        """
        Layer-by-Layer Spiral Traversal
        
        Approach: Process the matrix in layers from outside to inside
        Each layer completes: right → down → left → up
        
        Time Complexity: O(m × n) - visit each element once
        Space Complexity: O(1) - excluding output array
        """
        res = []
        
        # Initialize boundaries
        left, right = 0, len(matrix[0])  # Column boundaries (0 to n)
        top, bottom = 0, len(matrix)      # Row boundaries (0 to m)
        
        # Continue while there are elements to process
        while left < right and top < bottom:
            
            # STEP 1: Get every element in the top row (move right)
            # Traverse from left to right along the top boundary
            for i in range(left, right):
                res.append(matrix[top][i])
            top += 1  # Move top boundary down (this row is done)
            
            # STEP 2: Get every element in the right column (move down)
            # Traverse from top to bottom along the right boundary
            for i in range(top, bottom):
                res.append(matrix[i][right - 1])
            right -= 1  # Move right boundary left (this column is done)
            
            # Check if there are still rows/columns left to process
            # This prevents processing the same row/column twice in edge cases
            if not (left < right and top < bottom):
                break
            
            # STEP 3: Get every element in the bottom row (move left)
            # Traverse from right to left along the bottom boundary
            for i in range(right - 1, left - 1, -1):
                res.append(matrix[bottom - 1][i])
            bottom -= 1  # Move bottom boundary up (this row is done)
            
            # STEP 4: Get every element in the left column (move up)
            # Traverse from bottom to top along the left boundary
            for i in range(bottom - 1, top - 1, -1):
                res.append(matrix[i][left])
            left += 1  # Move left boundary right (this column is done)
        
        return res

