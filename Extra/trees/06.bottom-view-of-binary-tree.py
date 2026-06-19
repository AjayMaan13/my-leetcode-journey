"""
Bottom View of a Binary Tree
------------------------------

Problem Statement:
Given a Binary Tree, return its Bottom View — the set of nodes visible when
looking at the tree from below. For each vertical column, the bottom-most
node (last encountered in BFS) is included.

Example 1:
Input:  1 2 3 4 10 9 11 -1 5 -1 -1 -1 -1 -1 -1 -1 6
Output: [4, 5, 6, 3, 11]

Example 2:
Input:  2 7 5 2 6 -1 9 -1 -1 5 11 4 -1
Output: [2, 5, 6, 11, 4, 9]

Approach:
Identical to Top View except we always overwrite the map entry for a column
(instead of only writing on first visit). BFS processes nodes top-down, so
the last write per column is always the bottom-most node.

Related: Extra/trees/05.top-view-of-binary-tree.py
"""

from collections import deque


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def bottomView(self, root):
        ans = []
        if root is None:
            return ans

        mpp = {}
        q = deque([(root, 0)])  # (node, vertical column)

        while q:
            node, line = q.popleft()
            mpp[line] = node.data  # always overwrite → last = bottom-most
            if node.left:
                q.append((node.left, line - 1))
            if node.right:
                q.append((node.right, line + 1))

        for key in sorted(mpp):
            ans.append(mpp[key])

        return ans


if __name__ == "__main__":
    # Example 1: expected [4, 5, 6, 3, 11]
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(10)
    root.right.left = Node(9)
    root.right.right = Node(11)
    root.left.left.right = Node(5)
    root.left.left.right.right = Node(6)

    sol = Solution()
    print("Bottom View:", sol.bottomView(root))

    # Example 2: expected [2, 5, 6, 11, 4, 9]
    root2 = Node(2)
    root2.left = Node(7)
    root2.right = Node(5)
    root2.left.left = Node(2)
    root2.left.right = Node(6)
    root2.right.right = Node(9)
    root2.left.right.left = Node(5)
    root2.left.right.right = Node(11)
    root2.left.left.right = Node(4)

    print("Bottom View:", sol.bottomView(root2))
