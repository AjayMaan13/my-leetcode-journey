"""
Check for Children Sum Property in a Binary Tree
--------------------------------------------------

Problem Statement:
Given a Binary Tree, convert node values to follow the Children Sum Property:
every node's value must equal the sum of its children's values. Node values
can only be increased (never decreased); tree structure cannot change.

Example 1:
Input:  2 35 10 2 3 5 2
Output: 45 35 10 30 5 8 2

Example 2:
Input:  50 7 2 3 5 1 30
Output: 50 55 5 86 1 31 30

Approach:
Pre-order pass: at each node, compare node.val with child sum.
  - If child sum >= node.val  → raise node to match child sum.
  - If child sum < node.val   → raise one child to match node (can't lower node).
Then recurse into children so they satisfy the property below.
Post-order update: set node.val = left.val + right.val (children have been
finalised, so this is now correct).
"""


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class Solution:
    def changeTree(self, root):
        if root is None:
            return

        child = 0
        if root.left:
            child += root.left.val
        if root.right:
            child += root.right.val

        if child >= root.val:
            root.val = child
        else:
            # Can't lower the node, so raise a child to absorb the difference
            if root.left:
                root.left.val = root.val
            elif root.right:
                root.right.val = root.val

        self.changeTree(root.left)
        self.changeTree(root.right)

        # Post-order: update node to exact sum of (now-finalised) children
        tot = 0
        if root.left:
            tot += root.left.val
        if root.right:
            tot += root.right.val
        if root.left or root.right:
            root.val = tot


def inorder(root):
    if not root:
        return
    inorder(root.left)
    print(root.val, end=" ")
    inorder(root.right)


if __name__ == "__main__":
    # Example tree
    root = TreeNode(2)
    root.left = TreeNode(35)
    root.right = TreeNode(10)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(3)
    root.right.left = TreeNode(5)
    root.right.right = TreeNode(2)

    print("Before: ", end="")
    inorder(root)
    print()

    Solution().changeTree(root)

    print("After:  ", end="")
    inorder(root)
    print()
