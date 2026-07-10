"""
LeetCode Problem: 235. Lowest Common Ancestor of a Binary Search Tree
Link: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/

Description:
Given a BST, find the lowest common ancestor (LCA) of two given nodes p and q.
The LCA is the lowest node that has both p and q as descendants
(a node is allowed to be a descendant of itself).

Example 1:
         6
        / \\
       2   8
      / \\ / \\
     0  4 7  9
       / \\
      3   5

Input: p=2, q=8  → Output: 6  (6 is the split point)
Input: p=2, q=4  → Output: 2  (2 is an ancestor of 4; node counts as its own descendant)
"""

from collections import deque


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 1 — signal / count encoding (my original approach)
#
# DFS the entire tree. Each call returns how many of {p, q} it has found below.
# When a subtree's count + the current node's own match reaches 2, that node
# is the LCA — store it in self.res and propagate 0 to stop further searching.
#
# Works for any binary tree (does NOT exploit BST ordering).
# Time: O(n)  Space: O(h) recursion stack
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def lowestCommonAncestor_v1(self, root, p, q):
        if not root or not q or not p:
            return None

        self.res = None

        def signalNodes(node, p, q):
            if not node or self.res:
                return 0

            left  = signalNodes(node.left,  p, q)
            right = signalNodes(node.right, p, q)
            total = left + right

            if node == q or node == p:
                total += 1

            # Both targets found — this node is the LCA
            if total == 2:
                self.res = node
                return 0       # stop propagating; nothing above needs to know

            return total

        signalNodes(root, p, q)
        return self.res


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 2 — clean recursive (return-value style)
#
# Same idea but without a self.res accumulator.
# Base cases:
#   - hit None      → nothing found, return None
#   - hit p or q    → found one target, return it (stop descending this side)
# After both recursive calls:
#   - both left and right are non-None → p and q split here → current node is LCA
#   - only one side is non-None        → both targets live on that side; bubble it up
#
# Also works for any binary tree. Time: O(n)  Space: O(h)
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def lowestCommonAncestor_v2(self, root, p, q):
        # Reached a leaf's child, or found one of the targets → report up
        if not root or root == p or root == q:
            return root

        left  = self.lowestCommonAncestor_v2(root.left,  p, q)
        right = self.lowestCommonAncestor_v2(root.right, p, q)

        # p came from the left, q came from the right (or vice versa)
        # → this node is the split point → it is the LCA
        if left and right:
            return root

        # Both targets are on the same side — bubble up the non-None result
        return left or right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 3 — BST-specific (exploit ordering) ← most efficient for 235
#
# Because it's a BST, we know exactly which subtree to enter:
#   - both p and q < root → LCA must be in left subtree
#   - both p and q > root → LCA must be in right subtree
#   - they straddle root (or one equals root) → root IS the LCA
#
# No need to search both subtrees. Time: O(h)  Space: O(1) iterative / O(h) recursive
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        curr = root
        while curr:
            if p.val < curr.val and q.val < curr.val:
                curr = curr.left        # both targets are smaller → go left
            elif p.val > curr.val and q.val > curr.val:
                curr = curr.right       # both targets are larger  → go right
            else:
                return curr             # straddle (or one equals curr) → LCA found


# ─────────────────────────────────────────────────────────────────────────────
# Helpers for testing
# ─────────────────────────────────────────────────────────────────────────────
def buildTree(values):
    if not values:
        return None
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


def findNode(root, val):
    while root:
        if val == root.val:
            return root
        root = root.left if val < root.val else root.right
    return None


if __name__ == "__main__":
    sol = Solution()

    tree = buildTree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])

    test_cases = [
        (2, 8, 6),   # split at root
        (2, 4, 2),   # node is its own ancestor
        (3, 5, 4),   # both inside subtree
        (0, 5, 2),   # deep split
    ]

    for p_val, q_val, expected in test_cases:
        p = findNode(tree, p_val)
        q = findNode(tree, q_val)
        result = sol.lowestCommonAncestor(tree, p, q)
        status = "✅ Passed" if result.val == expected else "❌ Failed"
        print(f"{status}  p={p_val}, q={q_val} → LCA={result.val}  (expected {expected})")
