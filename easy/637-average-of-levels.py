"""
LeetCode Problem: Average of Levels in Binary Tree
Link: https://leetcode.com/problems/average-of-levels-in-binary-tree/

Prompt:
Given the root of a binary tree, return an array of the average value of the nodes 
on each level in the form of a list of floats.

Example:
Input: root = [3,9,20,None,None,15,7]
Output: [3.0, 14.5, 11.0]

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -2^31 <= Node.val <= 2^31 - 1
"""

from collections import deque

# TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# My Solution DFS
from collections import deque
class Solution(object):
    def averageOfLevels(self, root):
        if not root:
            return []

        queue = deque([root])
        result = []

        while queue:
            level_sum = 0
            level_size = len(queue)

            for _ in range(level_size):
                node = queue.popleft()
                level_sum += node.val

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(level_sum / float(level_size))

        return result

    
# Helper function to build a binary tree from a list (level order)
def build_tree(nodes):
    if not nodes or nodes[0] is None:
        return None
    
    root = TreeNode(nodes[0])
    queue = deque([root])
    i = 1
    while i < len(nodes):
        current = queue.popleft()
        if nodes[i] is not None:
            current.left = TreeNode(nodes[i])
            queue.append(current.left)
        i += 1
        
        if i < len(nodes) and nodes[i] is not None:
            current.right = TreeNode(nodes[i])
            queue.append(current.right)
        i += 1
    
    return root


# Test cases for validation
test_cases = [
    ([3, 9, 20, None, None, 15, 7], [3.0, 14.5, 11.0]),
    ([1, 2, 3, 4, 5, 6, 7], [1.0, 2.5, 5.5]),
    ([3,9,20,None,None,15,7], [3.0,14.5,11.0]),
]

solution = Solution()  # Your Solution class with averageOfLevels method

for i, (tree_list, expected) in enumerate(test_cases, 1):
    root = build_tree(tree_list)
    output = solution.averageOfLevels(root)
    print(f"Test case {i}:")
    print(f"Input tree: {tree_list}")
    print(f"Expected output: {expected}")
    print(f"Actual output:   {output}")
    print(f"Pass: {all(abs(a-b) < 1e-5 for a,b in zip(output, expected))}")
    print()
