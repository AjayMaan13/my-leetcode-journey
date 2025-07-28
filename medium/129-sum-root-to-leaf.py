"""
129. Sum Root to Leaf Numbers
-----------------------------

🔹 Problem Statement:
You are given the root of a binary tree containing digits from 0 to 9 only.

Each root-to-leaf path in the tree represents a number.

For example, the root-to-leaf path 1 -> 2 -> 3 represents the number 123.

Return the total sum of all root-to-leaf numbers.

A leaf node is a node with no children.

🔹 Example 1:
Input:  root = [1,2,3]
Output: 25
Explanation:
  Path 1->2 = 12
  Path 1->3 = 13
  Total = 12 + 13 = 25

🔹 Example 2:
Input:  root = [4,9,0,5,1]
Output: 1026
Explanation:
  Paths:
  4->9->5 = 495
  4->9->1 = 491
  4->0    = 40
  Total   = 495 + 491 + 40 = 1026

🔹 Constraints:
- The number of nodes in the tree is in the range [1, 1000].
- 0 <= Node.val <= 9
- The depth of the tree will not exceed 10.
"""

# 🔹 Definition for a binary tree node
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# My Solution class (DFS)
class Solution(object):
    def sumNumbers(self, root):
        if not root:
            return 0
        self.sum = 0

        def recursionSum(node, value):
            if not node:
                return False
            
            new_value = value * 10 + node.val
            
            # If leaf node → add to sum
            if not node.left and not node.right:
                self.sum += new_value
                return True  # return True so parent knows it's a leaf
            
            # Recurse on children
            left = recursionSum(node.left, new_value)
            right = recursionSum(node.right, new_value)

            return left or right  # return True if any child path exists

        recursionSum(root, 0)
        return self.sum

# Slightly Optimized Solution
class Solution(object):
    def sumNumbers(self, root):
        """
        DFS Approach - Functional style without using self.sum
        Time Complexity: O(n)
        Space Complexity: O(h) due to recursion stack
        """

        def dfs(node, value):
            if not node:
                return 0

            new_value = value * 10 + node.val

            # If leaf node, return the value
            if not node.left and not node.right:
                return new_value

            # Otherwise, recurse on both sides and return total
            return dfs(node.left, new_value) + dfs(node.right, new_value)

        return dfs(root, 0)


# 🔹 Tester Code
if __name__ == "__main__":
    # Example 1: root = [1,2,3]
    root1 = TreeNode(1)
    root1.left = TreeNode(2)
    root1.right = TreeNode(3)

    # Example 2: root = [4,9,0,5,1]
    root2 = TreeNode(4)
    root2.left = TreeNode(9)
    root2.right = TreeNode(0)
    root2.left.left = TreeNode(5)
    root2.left.right = TreeNode(1)

    sol = Solution()

    print("Example 1 Output:", sol.sumNumbers(root1))  # Expected: 25
    print("Example 2 Output:", sol.sumNumbers(root2))  # Expected: 1026
