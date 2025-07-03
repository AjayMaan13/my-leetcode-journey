# 104. Maximum Depth of Binary Tree
# https://leetcode.com/problems/maximum-depth-of-binary-tree/

# Given the root of a binary tree, return its maximum depth.
# A binary tree's maximum depth is the number of nodes along the longest path 
# from the root node down to the farthest leaf node.

# Example 1:
# Input: root = [3,9,20,null,null,15,7]
# Output: 3

# Example 2:
# Input: root = [1,null,2]
# Output: 2

# Constraints:
# The number of nodes in the tree is in the range [0, 10^4].
# -100 <= Node.val <= 100

# Definition for a binary tree node.

class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution(object):
    # My Solution
    def maxDepth(self, root):
        if not root:
            return 0
        
        leftDepth = self.maxDepth(root.left) if root.left else 0
        rightDepth = self.maxDepth(root.right) if root.right else 0

        return 1 + max(leftDepth, rightDepth)
    
     # Optimized BFS solution
    def maxDepthBFS(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        from collections import deque

        if not root:
            return 0

        queue = deque([root])
        depth = 0

        while queue:
            level_size = len(queue)  # Number of nodes at current depth
            for _ in range(level_size):
                node = queue.popleft()
                # Add children of current node to queue for next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            depth += 1  # Increment depth after processing all nodes at current level

        return depth

# Helper to build a binary tree from a list (level-order)
def build_tree_from_list(values):
    if not values:
        return None
    nodes = [None if val is None else TreeNode(val) for val in values]
    kids = nodes[::-1]
    root = kids.pop()
    for node in nodes:
        if node:
            if kids: node.left = kids.pop()
            if kids: node.right = kids.pop()
    return root

if __name__ == "__main__":
    sol = Solution()
    test_cases = [
        ([3, 9, 20, None, None, 15, 7], 3),
        ([1, None, 2], 2),
        ([], 0),
        ([0], 1)
    ]

    for i, (tree_list, expected) in enumerate(test_cases, 1):
        root = build_tree_from_list(tree_list)
        result = sol.maxDepth(root)
        print(f"Test Case {i}: maxDepth({tree_list}) = {result} (Expected: {expected})")
