"""
LeetCode 112: Path Sum

Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf 
path such that adding up all the values along the path equals targetSum.

A leaf is a node with no children.
"""

class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# My Solution (DFS)
class Solution(object):
    def hasPathSum(self, root, targetSum):
        if not root:
            return False
        
        if not root.left and not root.right:
            return targetSum == root.val
        
        return (self.hasPathSum(root.left, targetSum - root.val) or
                self.hasPathSum(root.right, targetSum - root.val))

    
# BFS / Iterative Approach (Queue-based)
from collections import deque
class Solution(object):
    def hasPathSum(self, root, targetSum):
        if not root:
            return False

        queue = deque([(root, root.val)])

        while queue:
            node, curr_sum = queue.popleft()

            if not node.left and not node.right and curr_sum == targetSum:
                return True

            if node.left:
                queue.append((node.left, curr_sum + node.left.val))
            if node.right:
                queue.append((node.right, curr_sum + node.right.val))

        return False


# --- Helper to build tree ---
def build_tree(values):
    """
    Builds a binary tree from level-order list. Use None for missing nodes.
    """
    if not values:
        return None
    nodes = [TreeNode(val) if val is not None else None for val in values]
    i = 1
    for node in nodes:
        if node:
            if i < len(nodes): node.left = nodes[i]; i += 1
            if i < len(nodes): node.right = nodes[i]; i += 1
    return nodes[0]

# --- Test cases ---
if __name__ == "__main__":
    sol = Solution()

    # Test 1
    root1 = build_tree([5,4,8,11,None,13,4,7,2,None,None,None,1])
    print("Test 1:", sol.hasPathSum(root1, 22))  # Expected: True

    # Test 2
    root2 = build_tree([1,2,3])
    print("Test 2:", sol.hasPathSum(root2, 5))  # Expected: False

    # Test 3
    print("Test 3:", sol.hasPathSum(None, 0))  # Expected: False

    # Test 4
    root4 = build_tree([1])
    print("Test 4:", sol.hasPathSum(root4, 1))  # Expected: True
