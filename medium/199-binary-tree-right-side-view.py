"""
LeetCode 199. Binary Tree Right Side View
-----------------------------------------

Given the root of a binary tree, imagine yourself standing on the right side of it,
return the values of the nodes you can see ordered from top to bottom.

Example 1:
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]

Example 2:
Input: root = [1,2,3,4,null,null,null,5]
Output: [1,3,4,5]

Example 3:
Input: root = [1,null,3]
Output: [1,3]

Example 4:
Input: root = []
Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 100].
-100 <= Node.val <= 100
"""


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# My Solution here
from collections import deque
class Solution(object):
    def rightSideView(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: List[int]
        """
        if not root:
            return []
        
        result = []
        queue = deque([root])

        while queue:
            result.append(queue[-1].val)

            for _ in range(len(queue)):
                node = queue.popleft()

                if node.left:
                    queue.append(node.left)

                if node.right:
                    queue.append(node.right)
        

        return result

# Helper: Build tree from list like [1,2,3,None,5]
def build_tree(values):
    if not values or values[0] is None:
        return None
    nodes = [TreeNode(val) if val is not None else None for val in values]
    child_index = 1
    for i in range(len(nodes)):
        if nodes[i] is not None:
            if child_index < len(nodes):
                nodes[i].left = nodes[child_index]
                child_index += 1
            if child_index < len(nodes):
                nodes[i].right = nodes[child_index]
                child_index += 1
    return nodes[0]

# Test cases
test_cases = [
    ([1,2,3,None,5,None,4], [1,3,4]),
    ([1,2,3,4,None,None,None,5], [1,3,4,5]),
    ([1,None,3], [1,3]),
    ([], []),
    ([1], [1]),
]

# Run tests
def run_tests():
    sol = Solution()
    for i, (tree_list, expected) in enumerate(test_cases):
        root = build_tree(tree_list)
        result = sol.rightSideView(root)
        print(f"Test Case {i+1}: {'PASS' if result == expected else 'FAIL'}")
        print(f"Input: {tree_list}")
        print(f"Expected: {expected}, Got: {result}")
        print("-----")

if __name__ == "__main__":
    run_tests()
