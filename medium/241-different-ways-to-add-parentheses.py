"""
LeetCode 241. Different Ways to Add Parentheses  |  Medium

Given a string expression of numbers and operators, return all possible results
from computing all the different ways to group numbers and operators.

Examples:
    "2-1-1"     → [0, 2]       ( (2-1)-1=0 , 2-(1-1)=2 )
    "2*3-4*5"   → [-34,-14,-10,-10,10]

Constraints:
    expression consists of digits and '+', '-', '*'.
    All integer values are in [0, 99].
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Divide and Conquer (Recursive, substring slicing)
# Time  : O(n * Catalan(n))  Space : O(n * Catalan(n))
#
# Key insight — "divide at every operator":
#   For each operator at position i, split the expression into:
#     LEFT  = expression[:i]     (everything before the operator)
#     RIGHT = expression[i+1:]   (everything after the operator)
#   Recursively get all results from LEFT and RIGHT, then combine every
#   pair (n1, n2) using the operator at i.
#
#   Base case: no operator found → the entire substring is a plain number.
#
# This naturally generates ALL possible parenthesizations because every
# way to add parentheses corresponds to choosing one operator as the "root"
# of the expression tree and recursing on both halves.
#
# e.g. "2-1-1":
#   split at i=1 ('-'): LEFT="2" → [2], RIGHT="1-1" → [0]
#     combine: 2-0 = 2
#   split at i=3 ('-'): LEFT="2-1" → [1], RIGHT="1" → [1]
#     combine: 1-1 = 0
#   result: [2, 0]  ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def diffWaysToCompute(self, expression: str):
        operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
        }

        res = []

        for i in range(len(expression)):
            op = expression[i]

            if op in operations:
                # divide: recurse on left and right subexpressions
                nums1 = self.diffWaysToCompute(expression[:i])      # LEFT half
                nums2 = self.diffWaysToCompute(expression[i + 1:])  # RIGHT half

                # conquer: combine every result pair using this operator
                for n1 in nums1:
                    for n2 in nums2:
                        res.append(operations[op](n1, n2))

        # base case: no operator found → whole expression is a single number
        if res == []:
            res.append(int(expression))

        return res


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: Backtracking with Index Range (no substring copying)
# Time  : O(n * Catalan(n))  Space : O(n * Catalan(n))  (same complexity)
#
# Same divide-and-conquer idea, but instead of slicing substrings we pass
# (left, right) index bounds into a nested helper function.
# This avoids creating new string objects on every recursive call.
#
# backtrack(left, right) computes all results for expression[left..right].
#   - Scan i from left to right; if expression[i] is an operator:
#       nums1 = backtrack(left, i-1)    ← left subexpression
#       nums2 = backtrack(i+1, right)   ← right subexpression
#       combine every pair with the operator
#   - If no operator found in [left..right], the segment is a number:
#       parse int(expression[left:right+1]) and return it
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def diffWaysToCompute(self, expression: str):
        operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
        }

        def backtrack(left, right):
            res = []

            for i in range(left, right + 1):    # scan the current window
                op = expression[i]

                if op in operations:
                    # split at this operator, recurse on both halves
                    nums1 = backtrack(left, i - 1)      # left subexpression
                    nums2 = backtrack(i + 1, right)     # right subexpression

                    # combine every pair of results using this operator
                    for n1 in nums1:
                        for n2 in nums2:
                            res.append(operations[op](n1, n2))

            # base case: no operator in [left..right] → single number
            if res == []:
                res.append(int(expression[left:right + 1]))

            return res

        return backtrack(0, len(expression) - 1)
