"""
LeetCode 222. Count Complete Tree Nodes
--------------------------------------

Given the root of a complete binary tree, return the number of nodes in the tree.

A complete binary tree is defined as:
- Every level, except possibly the last, is completely filled.
- All nodes in the last level are as far left as possible.

Goal:
Design an algorithm that runs in less than O(n) time complexity.

Examples:

Input: root = [1,2,3,4,5,6]
Output: 6

Input: root = []
Output: 0

Input: root = [1]
Output: 1

Constraints:
- The number of nodes in the tree is in the range [0, 5 * 10^4].
- 0 <= Node.val <= 5 * 10^4
- The tree is guaranteed to be complete.
"""

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right



# MY Solution 1 DFS, O(n)-time & O(1)-space
class Solution(object):
    def countNodes(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if not root:
            return 0

        def dfs(node):
            if not node:
                return 0
            return 1 + dfs(node.left) + dfs(node.right)

        return dfs(root)
# OR 
    def countNodes(self, root):
        """
        #:type root: Optional[TreeNode]
        #:rtype: int
        """

        if not root:
            return 0
        
        self.nodesSum = 0

        def recursion(node):
            if not node:
                return
            self.nodesSum +=1

            recursion(node.left)
            recursion(node.right)

        recursion(root)

        return self.nodesSum




# My Solution 2 (BFS), O(n)-time & O(n)-space
from collections import deque

    def countNodes(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if not root:
            return 0

        queue = deque([root])
        count = 0

        while queue:
            node = queue.popleft()
            count += 1  # Count this node

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        return count


# OR
from collections import deque
    def countNodes(self, root):
        
        #:type root: Optional[TreeNode]
        #:rtype: int
        

        if not root:
            return 0
        
        queue = deque([root])
        self.nodesNum = 1

        while queue:
            length = len(queue)
            for _ in range(length):
                node = queue.popleft()

                if node.left:
                    queue.append(node.left)
                    self.nodesNum += 1

                if node.right:
                    queue.append(node.right)
                    self.nodesNum += 1
        
        return self.nodesNum


# Best Optimized Solution, O(Log^2n) time
    def countNodes(self, root):
        """
        Counts the number of nodes in a COMPLETE binary tree
        in O(log^2 n) time using properties of a complete tree.

        In a COMPLETE Binary tree, the number of nodes are -> 2^h - 1, where h is height of the tree
        Example:
                1
               / \
              2   3
             / \  /\
            4  5 6  7

        Height = 3, 2^3 - 1 = 7
        But, height of sub-tree + root node = 2^h, where h is height of subtree
        Example in Left subtree, h = 2(from with 3, 6 and 7)
        Therefore, nodes = 2^2 = 4(including root node)
        """

        if not root:
            return 0

        # Function to get height of the leftmost path
        def getHeight(node):
            height = 0
            while node:
                height += 1
                node = node.left
            return height

        # Get heights of left and right subtrees
        left_h = getHeight(root.left)
        right_h = getHeight(root.right)

        """
        CASE 1: left_h == right_h
        ----------------------------------------
        Meaning: The LEFT subtree is PERFECT.

        Example:
                1
               / \
              2   3
             / \  /
            4  5 6

        At root = 1:
        left_h = 2 (2->4), right_h = 2 (3->6)

        Since they are equal -> left subtree has exactly 2^2 - 1 = 3 nodes.
        Total nodes in left subtree + root = 2^2 = 4.

        So count = 4 + countNodes(root.right)
        """

        if left_h == right_h:
            return (2 ** left_h) + self.countNodes(root.right)

        """
        # CASE 2: left_h != right_h → RIGHT subtree is perfect (but smaller)
        # Bigger Example for Case 2:
        #
        #               1
        #             /   \
        #            2     3
        #           / \   / \
        #          4   5 6   7
        #         / \
        #        8   9
        #
        # At root=1:
        #   left_h = 4 (1→2→4→8)
        #   right_h = 3 (1→3→6)
        #
        # Since left_h != right_h → right subtree is perfect.
        #
        # Formula:
        # count = 2^right_h + countNodes(root.left)
        #       = 2^3 + countNodes(root.left)
        #       = 8 + countNodes(root.left)
        """
        else:
            return (2 ** right_h) + self.countNodes(root.left)


