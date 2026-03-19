"""
84. Largest Rectangle in Histogram

Given an array heights where heights[i] is the height of the i-th bar (width=1),
return the area of the largest rectangle that fits in the histogram.

Example 1: heights = [2,1,5,6,2,3] -> 10  (bars 5,6 with height 5, width 2)
Example 2: heights = [2,4]          -> 4

Constraints:
- 1 <= heights.length <= 10^5
- 0 <= heights[i] <= 10^4

Key idea:
  Each bar i can be the MINIMUM height of some rectangle.
  The rectangle extends left and right as long as neighbouring bars are >= heights[i].
  Area = heights[i] * (right_boundary - left_boundary - 1)
"""

# ===== Brute Force =====
# For every pair (i, j), the rectangle spanning bars i..j has height = min(heights[i..j]).
# Track the running minimum as we extend j rightward to avoid recomputing.
# Time: O(n^2) | Space: O(1)

class SolutionBrute(object):
    def largestRectangleArea(self, heights):
        n    = len(heights)
        area = 0

        for i in range(n):
            min_h = heights[i]                      # shortest bar seen so far in this window
            for j in range(i, n):
                min_h  = min(min_h, heights[j])     # extend window, update minimum height
                width  = j - i + 1
                area   = max(area, min_h * width)

        return area


# ===== My Optimal Solution — Monotonic Stack (On-Pop, Single Pass) =====
#
# Think of each bar heights[i] as asking:
# "How far can I expand left and right while I remain the smallest height?"
#
# Use a monotonic INCREASING stack of indices.
# When we encounter a bar shorter than the stack top, the top can no longer
# extend rightward — so we pop it and compute its maximum rectangle NOW.
#
# On pop of index `popped`:
#   right boundary = i          (first bar to the right that is shorter)
#   left  boundary = stack[-1]  (first bar to the left that is shorter, after pop)
#   width = right - left - 1   (bars strictly between the two boundaries)
#           OR i if stack is empty (popped bar was the global minimum — spans full width)
#
# Sentinel height=0 at i=len(heights) forces all remaining stack elements to flush.
# Time: O(n) | Space: O(n)

class SolutionOptimal(object):
    def largestRectangleArea(self, heights):
        stack = []
        area  = 0

        for i in range(len(heights) + 1):
            height = heights[i] if i < len(heights) else 0  # sentinel flushes stack at end

            while stack and heights[stack[-1]] > height:
                popped = stack.pop()

                """
                For each index i, you want:

                width = distance between:

                nearest smaller element on the left
                nearest smaller element on the right

                📏 Then area: area = height[i] * width
                """

                #left = popped - stack[-1] if stack else popped + 1
                #right = i - popped

                # width is right boundary - left and if there's a boundary on
                # both left and right, its might take one area twice
                width = i - stack[-1] - 1 if stack else i  # full span when no left wall exists
                area  = max(heights[popped] * width, area)

            stack.append(i)

        return area


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    optimal = SolutionOptimal()

    test_cases = [
        ([2, 1, 5, 6, 2, 3], 10),
        ([2, 4],               4),
        ([1],                  1),
        ([1, 1],               2),
        ([6, 2, 5, 4, 5, 1, 6], 12),
        ([0, 0],               0),
        ([5, 5, 5, 5],        20),
    ]

    for heights, expected in test_cases:
        r1 = brute.largestRectangleArea(heights[:])
        r2 = optimal.largestRectangleArea(heights[:])
        status = "PASS" if r1 == expected and r2 == expected else "FAIL"
        print(f"{status} heights={heights} -> brute={r1}, optimal={r2} (expected {expected})")
