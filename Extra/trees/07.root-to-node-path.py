"""
Print Root to Node Path in a Binary Tree
-----------------------------------------

Problem Statement:
Given a Binary Tree and a target node value, return the path from the root
to that node. No two nodes share the same value; the node is guaranteed to exist.

Example 1:
Input:  Tree: 1 2 3 4 5 -1 -1 -1 -1, target = 7
Output: [1, 2, 5, 7]

Example 2:
Input:  Tree: 1 2 3 -1 -1 4 5 -1 -1 6, target = 6
Output: [1, 3, 5, 6]

Approach 1 (mine):
Recursive DFS — if the target is found, return [node.val]; propagate the
found sub-path upward by prepending the current node's value. If neither
subtree contains the target, return [].

Approach 2:
Backtracking DFS — maintain a running path list, appending each node on
entry and popping on backtrack. Return True as soon as the target is found,
leaving the path intact.
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# Approach 1 — functional, builds path on the way back up
def rootToNodePath(root, target):
    def dfs(node, target):
        if not node:
            return []
        if node.val == target:
            return [node.val]
        left = dfs(node.left, target)
        if left:
            return [node.val] + left
        right = dfs(node.right, target)
        if right:
            return [node.val] + right
        return []

    return dfs(root, target)


# Approach 2 — backtracking, mutates a shared path list
class Solution:
    def rootToNodePath(self, root, target):
        path = []

        def dfs(node):
            if not node:
                return False
            path.append(node.val)
            if node.val == target:
                return True
            if dfs(node.left) or dfs(node.right):
                return True
            path.pop()
            return False

        dfs(root)
        return path


if __name__ == "__main__":
    # Example 1: expected [1, 2, 5, 7]
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.left.right.left = TreeNode(7)

    print("Approach 1:", rootToNodePath(root, 7))
    print("Approach 2:", Solution().rootToNodePath(root, 7))

    # Example 2: expected [1, 3, 5, 6]
    root2 = TreeNode(1)
    root2.left = TreeNode(2)
    root2.right = TreeNode(3)
    root2.right.left = TreeNode(4)
    root2.right.right = TreeNode(5)
    root2.right.right.left = TreeNode(6)

    print("Approach 1:", rootToNodePath(root2, 6))
    print("Approach 2:", Solution().rootToNodePath(root2, 6))
