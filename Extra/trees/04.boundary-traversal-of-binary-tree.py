"""
Boundary Traversal of a Binary Tree
-------------------------------------

Problem Statement:
Given a Binary Tree, perform the boundary traversal in anticlockwise direction
starting from the root. The boundary consists of:
  1. Root (if not a leaf)
  2. Left boundary  — top-down, excluding leaves
  3. All leaf nodes — left-to-right
  4. Right boundary — bottom-up, excluding leaves

Example 1:
Input:  1 2 7 3 -1 -1 8 -1 4 9 -1 5 6 10 11
Output: [1, 2, 3, 4, 5, 6, 10, 11, 9, 8, 7]

Example 2:
Input:  10 5 20 3 8 18 25 -1 7 -1 -1
Output: [10, 5, 3, 7, 8, 18, 25, 20]

Approach:
- Left boundary: walk left (fall to right if no left child), skip leaves.
- Leaves: preorder traversal, add only leaf nodes.
- Right boundary: walk right (fall to left if no right child), skip leaves,
  collect into a temp list then reverse before appending.
"""


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def isLeaf(self, node):
        return not node.left and not node.right

    def addLeftBoundary(self, root, res):
        curr = root.left
        while curr:
            if not self.isLeaf(curr):
                res.append(curr.data)
            curr = curr.left if curr.left else curr.right

    def addRightBoundary(self, root, res):
        curr = root.right
        temp = []
        while curr:
            if not self.isLeaf(curr):
                temp.append(curr.data)
            curr = curr.right if curr.right else curr.left
        res.extend(reversed(temp))

    def addLeaves(self, root, res):
        if self.isLeaf(root):
            res.append(root.data)
            return
        if root.left:
            self.addLeaves(root.left, res)
        if root.right:
            self.addLeaves(root.right, res)

    def printBoundary(self, root):
        res = []
        if not root:
            return res
        if not self.isLeaf(root):
            res.append(root.data)
        self.addLeftBoundary(root, res)
        self.addLeaves(root, res)
        self.addRightBoundary(root, res)
        return res


if __name__ == "__main__":
    # Example 1: expected [1, 2, 3, 4, 5, 6, 10, 11, 9, 8, 7]
    root = Node(1)
    root.left = Node(2)
    root.right = Node(7)
    root.left.left = Node(3)
    root.right.right = Node(8)
    root.left.left.right = Node(4)
    root.right.right.left = Node(9)
    root.left.left.right.left = Node(5)
    root.left.left.right.right = Node(6)
    root.right.right.left.left = Node(10)
    root.right.right.left.right = Node(11)

    sol = Solution()
    print("Boundary Traversal:", sol.printBoundary(root))

    # Example 2: expected [10, 5, 3, 7, 8, 18, 25, 20]
    root2 = Node(10)
    root2.left = Node(5)
    root2.right = Node(20)
    root2.left.left = Node(3)
    root2.left.right = Node(8)
    root2.right.left = Node(18)
    root2.right.right = Node(25)
    root2.left.left.right = Node(7)

    print("Boundary Traversal:", sol.printBoundary(root2))
