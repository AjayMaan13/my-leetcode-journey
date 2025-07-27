"""
102. Binary Tree Level Order Traversal
--------------------------------------

🔹 Problem Statement:
Given the root of a binary tree, return the level order traversal of its nodes' values.
(i.e., from left to right, level by level).

Example 1:
Input:  root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]

Example 2:
Input:  root = [1]
Output: [[1]]

Example 3:
Input:  root = []
Output: []

Constraints:
- The number of nodes in the tree is in the range [0, 2000].
- -1000 <= Node.val <= 1000
"""

from collections import deque

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution(object):
    def levelOrder(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: List[List[int]]
        """

        # If the tree is empty
        if not root:
            return []

        result = []  # Final output list
        queue = deque([root])  # BFS queue starting with root node

        while queue:
            level_size = len(queue)  # Number of nodes in current level
            current_level = []       # Store all values of this level

            for _ in range(level_size):
                node = queue.popleft()       # Remove node from queue
                current_level.append(node.val)

                # Add children to the queue for the next level
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

            # After processing the level, add to result
            result.append(current_level)

        return result


"""
🔹 How it works (BFS approach):
--------------------------------
Example: root = [3,9,20,null,null,15,7]

Step 1: queue = [3] → current_level = [3] → result = [[3]]
Step 2: queue = [9,20] → current_level = [9,20] → result = [[3],[9,20]]
Step 3: queue = [15,7] → current_level = [15,7] → result = [[3],[9,20],[15,7]]

✅ Output = [[3],[9,20],[15,7]]
"""

# -------------------------
# 🔹 Example Usage
# -------------------------
if __name__ == "__main__":
    # Build example tree: [3,9,20,null,null,15,7]
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)

    sol = Solution()
    print(sol.levelOrder(root))  # Expected Output: [[3], [9, 20], [15, 7]]
