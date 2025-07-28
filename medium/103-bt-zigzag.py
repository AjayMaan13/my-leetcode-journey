"""
103. Binary Tree Zigzag Level Order Traversal

Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. 
(i.e., from left to right, then right to left for the next level and alternate between).

Example 1:
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[20,9],[15,7]]

Example 2:
Input: root = [1]
Output: [[1]]

Example 3:
Input: root = []
Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 2000].
-100 <= Node.val <= 100
"""

# -------------------------------
# Write your solution here
# -------------------------------

# My solution
from collections import deque
class Solution(object):
    def zigzagLevelOrder(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: List[List[int]]
        """
        if not root:
            return []

        result = []
        self.rightSideLoop = 0 # Not efficient
        queue = deque([root])

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft() 
                if self.rightSideLoop:
                    current_level.insert(0,node.val) # Not Efficient
                else:
                    current_level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            result.append(current_level)
            self.rightSideLoop = not self.rightSideLoop


        return result

# Optimized Solution, without (self.rightSideLoop & insert(0, node.val))
from collections import deque

class Solution(object):
    def zigzagLevelOrder(self, root):
        if not root:
            return []

        result = []
        queue = deque([root])
        left_to_right = True  # Track direction

        while queue:
            level_size = len(queue)
            current_level = []

            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node.val)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # Reverse if right-to-left
            if not left_to_right:
                current_level.reverse()

            result.append(current_level)
            left_to_right = not left_to_right  # Toggle direction

        return result




# -------------------------------
# Tester Code
# -------------------------------

class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_test_tree():
    # Build test tree: [3,9,20,null,null,15,7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    return root

if __name__ == "__main__":
    solution = Solution()
    root = build_test_tree()
    print("Expected Output: [[3], [20, 9], [15, 7]]")
    print("Your Output   :", solution.zigzagLevelOrder(root))
