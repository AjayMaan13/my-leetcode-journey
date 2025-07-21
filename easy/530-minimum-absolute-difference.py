"""
LeetCode Problem: 530. Minimum Absolute Difference in BST
Link: https://leetcode.com/problems/minimum-absolute-difference-in-bst/

Description:
Given the root of a Binary Search Tree (BST), return the minimum absolute 
difference between the values of any two different nodes in the tree.

Example 1:
Input: root = [4,2,6,1,3]
Output: 1

Example 2:
Input: root = [1,0,48,null,null,12,49]
Output: 1

Constraints:
- The number of nodes in the tree is in the range [2, 10^4].
- 0 <= Node.val <= 10^5

Note: This question is the same as 783.
"""

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# My Solution O(n^2) Not Ideal:
from collections import deque
class Solution(object):
    def getMinimumDifference(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        if not root:
            return

        queue = deque([root])
        all_nodes_value = []

        while queue:
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()
                all_nodes_value.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        mad = abs(all_nodes_value[0] - all_nodes_value[1])

        for i in all_nodes_value:
            for j in all_nodes_value:
                if i == j:
                    continue
                if abs(i - j) < mad:
                    mad = abs(i-j)
        
        return mad

# Optimized Solution O(nLog(n))
class Solution(object):
    def getMinimumDifference(self, root):
        values = []

        def dfs(node):
            if not node:
                return
            values.append(node.val)
            dfs(node.left)
            dfs(node.right)

        dfs(root)

        values.sort()  # sort values to compare neighbors

        min_diff = float('inf')
        for i in range(1, len(values)):
            min_diff = min(min_diff, abs(values[i] - values[i - 1]))

        return min_diff


# If its a BST:
"""We can use inorder traversal, because it always gives a sorted return"""
class Solution(object):
    def getMinimumDifference(self, root):
        self.prev = None      # Last visited value
        self.min_diff = float('inf')  # Smallest difference found

        def inorder(node):
            if not node:
                return

            inorder(node.left)   # Left

            # Visit this node
            if self.prev is not None:
                self.min_diff = min(self.min_diff, abs(node.val - self.prev))
            self.prev = node.val

            inorder(node.right)  # Right

        inorder(root)
        return self.min_diff



# -------------------------
# Testing code
# -------------------------

def build_tree_from_list(values):
    """Helper to build tree from level-order list."""
    if not values:
        return None
    from collections import deque
    root = TreeNode(values[0])
    queue = deque([root])
    index = 1
    while queue and index < len(values):
        node = queue.popleft()
        if values[index] is not None:
            node.left = TreeNode(values[index])
            queue.append(node.left)
        index += 1
        if index < len(values) and values[index] is not None:
            node.right = TreeNode(values[index])
            queue.append(node.right)
        index += 1
    return root


if __name__ == "__main__":
    # Test case 1
    root1 = build_tree_from_list([4, 2, 6, 1, 3])
    print("Expected: 1")
    print("Output:", Solution().getMinimumDifference(root1))

    # Test case 2
    root2 = build_tree_from_list([1, 0, 48, None, None, 12, 49])
    print("Expected: 1")
    print("Output:", Solution().getMinimumDifference(root2))
