"""
118. Pascal's Triangle
Easy

Given an integer numRows, return the first numRows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it.

Example 1:
Input: numRows = 5
Output: [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]

Visualization:
        1
       1 1
      1 2 1
     1 3 3 1
    1 4 6 4 1

Example 2:
Input: numRows = 1
Output: [[1]]

Constraints:
- 1 <= numRows <= 30
"""


class Solution(object):
    def generate_original(self, numRows):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach:
        - Create each row with all 1s
        - Fill middle elements by adding two elements from previous row
        
        Issues:
        1. Unnecessary check: if numRows < 1 (constraints guarantee numRows >= 1)
        2. Returns None instead of [] for invalid input
        3. Condition: if i - 1 > 0 is confusing
           - More intuitive: if i > 1 or if i >= 2
           - When i = 0: first row [1], no previous row
           - When i = 1: second row [1,1], no middle elements
           - When i = 2: third row [1,2,1], need to fill middle
        
        Time Complexity: O(numRows²) - generating all elements
        Space Complexity: O(1) - excluding output array
        """
        if numRows < 1:
            return  # Returns None instead of []
        
        output = []
        
        for i in range(numRows):
            # Create row with all 1s
            row = [1] * (i + 1)
            
            # Fill middle elements (if any)
            if i > 1:  # Confusing condition: means i >= 2
                for j in range(1, i):
                    row[j] = output[i - 1][j - 1] + output[i - 1][j]
            
            output.append(row)
        
        return output
    
    def generate_iterative_prev_row(self, numRows):
        """
        ALTERNATIVE: Build from Previous Row (Most Intuitive)
        
        Approach:
        - Start with first row [1]
        - Each new row: add 1 at start, compute middle elements, add 1 at end
        
        Key Insight:
        - Previous row helps generate current row
        - No need to access triangle[i-1], just use prev_row variable
        
        Time Complexity: O(numRows²)
        Space Complexity: O(1) - excluding output
        """
        triangle = [[1]]  # Start with first row
        
        for i in range(1, numRows):
            prev_row = triangle[-1]  # Get last row
            row = [1]  # Start with 1
            
            # Add middle elements
            for j in range(len(prev_row) - 1):
                row.append(prev_row[j] + prev_row[j + 1])
            
            row.append(1)  # End with 1
            triangle.append(row)
        
        return triangle
    
    def generate_pythonic(self, numRows):
        """
        PYTHONIC SOLUTION (Most Concise)
        
        Uses list comprehension for elegance
        
        Time Complexity: O(numRows²)
        Space Complexity: O(1) - excluding output
        """
        triangle = [[1]]
        
        for i in range(1, numRows):
            prev = triangle[-1]
            # Use zip to pair adjacent elements
            row = [1] + [prev[j] + prev[j + 1] for j in range(len(prev) - 1)] + [1]
            triangle.append(row)
        
        return triangle
    
    def generate_zip_approach(self, numRows):
        """
        MOST ELEGANT: Using zip()
        
        zip pairs adjacent elements automatically!
        
        Example: prev = [1, 2, 1]
        zip([0] + prev, prev + [0]) gives:
        (0, 1), (1, 2), (2, 1), (1, 0)
        
        Summing pairs: [1, 3, 3, 1] ✓
        
        Time Complexity: O(numRows²)
        Space Complexity: O(1) - excluding output
        """
        triangle = [[1]]
        
        for _ in range(1, numRows):
            prev = triangle[-1]
            # Pad with 0s and zip adjacent pairs
            row = [a + b for a, b in zip([0] + prev, prev + [0])]
            triangle.append(row)
        
        return triangle
    


"""
DETAILED EXPLANATION: How Pascal's Triangle Works

Pattern Recognition:
-------------------
Row 0:                    1
Row 1:                  1   1
Row 2:                1   2   1
Row 3:              1   3   3   1
Row 4:            1   4   6   4   1
Row 5:          1   5  10  10   5   1

Key Properties:
1. Each row starts and ends with 1
2. Each row has (row_index + 1) elements
3. Middle elements: sum of two elements directly above


Step-by-Step Generation (numRows = 5):
---------------------------------------

Row 0 (i = 0):
  row = [1]
  No middle elements
  triangle = [[1]]

Row 1 (i = 1):
  row = [1, 1]
  No middle elements (need i >= 2)
  triangle = [[1], [1,1]]

Row 2 (i = 2):
  row = [1, 1, 1]
  Middle element (j = 1):
    row[1] = triangle[1][0] + triangle[1][1] = 1 + 1 = 2
  row = [1, 2, 1]
  triangle = [[1], [1,1], [1,2,1]]

Row 3 (i = 3):
  row = [1, 1, 1, 1]
  Middle elements:
    j = 1: row[1] = triangle[2][0] + triangle[2][1] = 1 + 2 = 3
    j = 2: row[2] = triangle[2][1] + triangle[2][2] = 2 + 1 = 3
  row = [1, 3, 3, 1]
  triangle = [[1], [1,1], [1,2,1], [1,3,3,1]]

Row 4 (i = 4):
  row = [1, 1, 1, 1, 1]
  Middle elements:
    j = 1: row[1] = triangle[3][0] + triangle[3][1] = 1 + 3 = 4
    j = 2: row[2] = triangle[3][1] + triangle[3][2] = 3 + 3 = 6
    j = 3: row[3] = triangle[3][2] + triangle[3][3] = 3 + 1 = 4
  row = [1, 4, 6, 4, 1]
  triangle = [[1], [1,1], [1,2,1], [1,3,3,1], [1,4,6,4,1]]


Visual Understanding:
--------------------
        1              ← Row 0: Just 1
       / \
      1   1            ← Row 1: Two 1s
     / \ / \
    1   2   1          ← Row 2: Edges are 1, middle is 1+1=2
   / \ / \ / \
  1   3   3   1        ← Row 3: 1, 1+2=3, 2+1=3, 1
 / \ / \ / \ / \
1   4   6   4   1      ← Row 4: 1, 1+3=4, 3+3=6, 3+1=4, 1

Each number is the sum of the two numbers above it!


Why Your Condition "i - 1 > 0" is Confusing:
-------------------------------------------

Your code: if i - 1 > 0
  - When i = 0: i - 1 = -1, not > 0 ✓ (correct, no middle elements)
  - When i = 1: i - 1 = 0, not > 0 ✓ (correct, no middle elements)
  - When i = 2: i - 1 = 1, which is > 0 ✓ (correct, has middle element)

More intuitive: if i >= 2
  - Directly states: "need at least row 2 (third row) to have middle elements"
  - Easier to understand intent


Complexity Analysis:
-------------------

Time: O(numRows²)
  - Row 0: 1 operation
  - Row 1: 2 operations
  - Row 2: 3 operations
  - ...
  - Row n-1: n operations
  - Total: 1 + 2 + 3 + ... + n = n(n+1)/2 = O(n²)

Space: O(1) excluding output
  - Only use constant extra space for loop variables
  - Output array is required and doesn't count


Mathematical Connection:
-----------------------

Pascal's Triangle is related to:
1. Binomial Coefficients: triangle[n][k] = C(n, k) = n! / (k! * (n-k)!)
2. Combinatorics: number of ways to choose k items from n items
3. Powers of 2: sum of row n = 2^n
   Row 0: 1 = 2^0
   Row 1: 1 + 1 = 2 = 2^1
   Row 2: 1 + 2 + 1 = 4 = 2^2
   Row 3: 1 + 3 + 3 + 1 = 8 = 2^3


Real-World Applications:
------------------------
1. Probability & Statistics (binomial distribution)
2. Algebra (binomial expansion)
3. Number Theory (properties of combinations)
4. Computer Science (dynamic programming example)
"""