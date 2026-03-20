"""
LeetCode 85. Maximal Rectangle  |  Hard

Given a binary matrix of '0's and '1's, find the largest rectangle
containing only '1's and return its area.

Examples:
    [["1","0","1","0","0"],
     ["1","0","1","1","1"],
     ["1","1","1","1","1"],   → 6
     ["1","0","0","1","0"]]

    [["0"]] → 0
    [["1"]] → 1

Key idea:
    Reduce to "Largest Rectangle in Histogram" (LC 84) row by row.
    heights[r][c] = number of consecutive '1's ending at row r in column c.
    Each row's heights array IS a histogram → apply LC 84 on each row.
"""


# ─────────────────────────────────────────────────────────────────────────────
# MY SOLUTION: 2D Heights + Per-row Histogram
# Time  : O(rows * cols),  Space : O(rows * cols)
#
# Step 1 — Build full 2D heights array:
#   heights[r][c] = count of consecutive '1's going UP from (r,c).
#   If matrix[r][c] == '0', reset count to 0.
#
# Step 2 — For each row, run the LC84 monotonic stack algorithm on that row's
#   heights to find the max rectangle that has its BOTTOM EDGE on row r.
#
# LC84 monotonic stack logic:
#   Maintain a stack of column indices in INCREASING height order.
#   When heights[r][c] < heights[r][stack top]:
#     → the stack top bar can't extend right → pop and compute its area.
#     width = c - stack[-1] - 1  (left boundary is the new stack top + 1)
#           = c                  (if stack is empty, bar extends to col 0)
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def maximalRectangle(self, matrix):
        row = len(matrix)
        col = len(matrix[0])
        heights = [[0] * col for _ in range(row)]

        for c in range(col):
            count = 0
            for r in range(row):
                if matrix[r][c] == "1":
                    count += 1
                    heights[r][c] = count
                else:
                    count = 0
                #print(f"heights[{r}][{c}]: {heights[r][c]}, count: {count}")

        #print(heights)

        areaMaxPerRow = 0
        for r in range(row):
            stack = []
            area = 0
            for c in range(col + 1):
                cur = heights[r][c] if c < col else 0   # sentinel 0 flushes remaining stack
                while stack and heights[r][stack[-1]] > cur:
                    popped = stack.pop()

                    # width: (stack[-1] + 1) → (c - 1)
                    width = c - stack[-1] - 1 if stack else c
                    areaMaxPerRow = max(areaMaxPerRow, heights[r][popped] * width)

                stack.append(c)

        #print(areaPerRow)

        return areaMaxPerRow


# ─────────────────────────────────────────────────────────────────────────────
# OPTIMIZED: 1D Rolling Heights (same algorithm, less space)
# Time  : O(rows * cols),  Space : O(cols)
#
# Exact same logic, but instead of storing the full 2D heights matrix,
# we keep a single 1D array and update it row by row in-place.
# This cuts space from O(rows*cols) → O(cols).
#
# The largestInHistogram helper is the same LC84 stack logic, just extracted
# into a clean function so the main loop reads clearly.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def maximalRectangle(self, matrix) -> int:

        def largestInHistogram(heights):
            # LC 84 — monotonic stack on a single row's heights
            stack = []
            max_area = 0

            for c in range(len(heights) + 1):
                cur = heights[c] if c < len(heights) else 0  # sentinel flushes stack

                while stack and heights[stack[-1]] > cur:
                    h = heights[stack.pop()]
                    w = c - stack[-1] - 1 if stack else c
                    max_area = max(max_area, h * w)

                stack.append(c)

            return max_area

        cols = len(matrix[0])
        heights = [0] * cols       # 1D rolling array — updated each row in-place

        best = 0
        for row in matrix:
            # update heights: extend bar if '1', reset to 0 if '0'
            for c in range(cols):
                heights[c] = heights[c] + 1 if row[c] == "1" else 0

            # treat current heights as a histogram and find max rectangle
            best = max(best, largestInHistogram(heights))

        return best
