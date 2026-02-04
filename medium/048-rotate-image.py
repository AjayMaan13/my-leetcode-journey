"""
48. Rotate Image
Medium

You are given an n x n 2D matrix representing an image, rotate the image by 
90 degrees (clockwise).

You have to rotate the image in-place, which means you have to modify the input 
2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

Example 1:
Input: matrix = [[1,2,3],[4,5,6],[7,8,9]]
Output: [[7,4,1],[8,5,2],[9,6,3]]

Visualization:
[1, 2, 3]      [7, 4, 1]
[4, 5, 6]  ->  [8, 5, 2]
[7, 8, 9]      [9, 6, 3]

Example 2:
Input: matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
Output: [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]

Visualization:
[5,  1,  9, 11]      [15, 13, 2,  5]
[2,  4,  8, 10]  ->  [14, 3,  4,  1]
[13, 3,  6,  7]      [12, 6,  8,  9]
[15, 14, 12, 16]     [16, 7, 10, 11]

Constraints:
- n == matrix.length == matrix[i].length
- 1 <= n <= 20
- -1000 <= matrix[i][j] <= 1000
"""


class Solution(object):
    def rotate_transpose_reflect(self, matrix):
        """
        APPROACH 1: Transpose + Reflect (Most Intuitive)
        
        Key Insight:
        Rotating 90° clockwise = Transpose + Reverse each row
        
        Steps:
        1. Transpose: Swap matrix[i][j] with matrix[j][i]
        2. Reflect: Reverse each row
        
        Example:
        [1, 2, 3]      Transpose     [1, 4, 7]      Reflect      [7, 4, 1]
        [4, 5, 6]   ------------>    [2, 5, 8]   ----------->   [8, 5, 2]
        [7, 8, 9]                    [3, 6, 9]                  [9, 6, 3]
        
        Time Complexity: O(n²) - visit each element twice
        Space Complexity: O(1) - in-place modifications
        """
        n = len(matrix)
        
        # Step 1: Transpose (swap along diagonal)
        for i in range(n):
            for j in range(i + 1, n):  # j starts from i+1 to avoid double-swapping
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
        
        # Step 2: Reverse each row
        for i in range(n):
            matrix[i].reverse()
            # Or manually: matrix[i] = matrix[i][::-1]
    
    def rotate_layer_by_layer(self, matrix):
        """
        APPROACH 2: Layer-by-Layer Rotation (Optimal)
        
        Key Insight:
        Rotate outer layer, then rotate inner layers recursively
        Think of the matrix as concentric squares
        
        Algorithm:
        - For each layer (outer to inner)
        - Rotate 4 cells at a time in a cycle:
          top -> right -> bottom -> left -> top
        
        Example for 3x3:
        Layer 0 (outer): Rotate 4 corners + 4 edges
        Layer 1 (inner): Just the center (no rotation needed)
        
        Visualization of one rotation cycle:
        
        top                           right
        [0,0] -------------------> [0,n-1]
          ^                          |
          |                          |
          |                          v
        [n-1,0] <--------------- [n-1,n-1]
        left                        bottom
        
        Time Complexity: O(n²) - visit each element once
        Space Complexity: O(1) - only temporary variables
        """
        n = len(matrix)
        left, right = 0, n - 1
        
        # Process each layer
        while left < right:
            top, bottom = left, right
            
            # Rotate elements in current layer
            for i in range(right - left):
                # Save top element
                temp = matrix[top][left + i]
                
                # Move left to top
                matrix[top][left + i] = matrix[bottom - i][left]
                
                # Move bottom to left
                matrix[bottom - i][left] = matrix[bottom][right - i]
                
                # Move right to bottom
                matrix[bottom][right - i] = matrix[top + i][right]
                
                # Move temp (original top) to right
                matrix[top + i][right] = temp
            
            # Move to inner layer
            left += 1
            right -= 1
    
    def rotate_four_way_swap(self, matrix):
        """
        APPROACH 3: Four-Way Swap (Clean & Efficient)
        
        Key Insight:
        Rotate 4 positions simultaneously in one operation
        
        For each layer, swap 4 elements:
        - top-left -> top-right
        - top-right -> bottom-right
        - bottom-right -> bottom-left
        - bottom-left -> top-left
        
        Time Complexity: O(n²)
        Space Complexity: O(1)
        """
        n = len(matrix)
        
        for layer in range(n // 2):
            first = layer
            last = n - 1 - layer
            
            for i in range(first, last):
                offset = i - first
                
                # Save top
                top = matrix[first][i]
                
                # left -> top
                matrix[first][i] = matrix[last - offset][first]
                
                # bottom -> left
                matrix[last - offset][first] = matrix[last][last - offset]
                
                # right -> bottom
                matrix[last][last - offset] = matrix[i][last]
                
                # top -> right
                matrix[i][last] = top
    
    def rotate_pythonic(self, matrix):
        """
        APPROACH 4: Pythonic One-Liner
        
        Uses Python's zip and unpacking features
        
        Explanation:
        - zip(*matrix) transposes the matrix
        - [::-1] reverses each row
        - matrix[:] = [...] modifies in-place
        
        Time Complexity: O(n²)
        Space Complexity: O(n²) - creates new lists (not truly in-place)
        """
        matrix[:] = [list(row)[::-1] for row in zip(*matrix)]
    
    # Main rotate function - uses the transpose + reflect approach
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        self.rotate_transpose_reflect(matrix)
