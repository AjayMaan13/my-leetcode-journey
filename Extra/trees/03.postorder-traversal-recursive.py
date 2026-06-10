"""
Postorder Traversal of Binary Tree (Recursive)
-----------------------------------------------

Problem Statement:
Given the root of a Binary Tree, return the postorder traversal
(Left → Right → Root) using recursion.

Example 1:
Input:  4 2 5 3 -1 7 6 -1 9 -1 -1 8 -1 1
Output: [1, 9, 3, 2, 7, 8, 6, 5, 4]

Example 2:
Input:  1 2 3 4 5 6 7 -1 -1 8 -1 -1 -1 9 10
Output: [4, 8, 5, 2, 6, 9, 10, 7, 3, 1]

Approach:
Pass the result list as a parameter so the same list is shared
across all recursive calls — avoids building sub-lists and merging.

Related: easy/145-binary-tree-postorder-traversal.py
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def postorderTraversal(self, root, result=None):
        if result is None:
            result = []
        if not root:
            return result
        self.postorderTraversal(root.left, result)
        self.postorderTraversal(root.right, result)
        result.append(root.val)
        return result


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    sol = Solution()
    result = []
    sol.postorderTraversal(root, result)
    print("Postorder traversal:", *result)
