"""
LeetCode Problem: 98. Validate Binary Search Tree
Link: https://leetcode.com/problems/validate-binary-search-tree/

Description:
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as:
1. The left subtree of a node contains only nodes with keys strictly less than the node's key.
2. The right subtree of a node contains only nodes with keys strictly greater than the node's key.
3. Both the left and right subtrees must also be binary search trees.

Example 1:
Input: root = [2,1,3]
Output: true

Example 2:
Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -2^31 <= Node.val <= 2^31 - 1
"""

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution(object):
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        if not root:
            return
        
        isBST = True
        self.leftVal = None

        # Get the Left Most node Val
        curr = root
        while curr.left:
            curr = curr.left
        
        leftVal = curr.val
        
        def inorder(leftVal, root):

            if not root:
                return
            
            inorder(leftVal, root.left)

            print(f"leftVal: {leftVal}, root: {root.val}")
            if root.val >= leftVal:
                isBST = False

            leftVal = root.val
            inorder(leftVal, root.right)

        inorder(leftVal, root)

        return isBST

"""class Solution(object):
    def isValidBST(self, root):
        
        #:type root: TreeNode
        #:rtype: bool
        
        if not root:
            return
        
        isBST = True
        inorderList = []

        def inorder(root):
            
            if not root:
                return
            inorder(root.left)
            inorderList.append(root.val)
            inorder(root.right)

        inorder(root)
        length = len(inorderList) 
        left = 0
        right = 1
        while right < length:
            if inorderList[left] >= inorderList[right]:
                isBST = False
            left += 1
            right += 1
        
        return isBST"""


    
# ----------------------
# Testing Code
# ----------------------

def build_tree_from_list(values):
    """Helper to build tree from level-order list."""
    if not values:
        return None

    from collections import deque
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


if __name__ == "__main__":
    # Test Case 1
    root1 = build_tree_from_list([2, 1, 3])
    print("Expected: True")
    print("Output:", Solution().isValidBST(root1))

    # Test Case 2
    root2 = build_tree_from_list([5, 1, 4, None, None, 3, 6])
    print("Expected: False")
    print("Output:", Solution().isValidBST(root2))

    root3 = build_tree_from_list([2,2,2])
    print("Expected: False")
    print("Output:", Solution().isValidBST(root3))
