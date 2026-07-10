"""
LeetCode Problem: 653. Two Sum IV - Input is a BST
Link: https://leetcode.com/problems/two-sum-iv-input-is-a-bst/

Description:
Given the root of a BST and an integer k, return true if there exist
two elements in the BST whose sum equals k.

Example 1: root = [5,3,6,2,4,null,7], k = 9  → True  (2+7 or 3+6)
Example 2: root = [5,3,6,2,4,null,7], k = 28 → False

Note: a node cannot pair with itself (two distinct elements required).
"""

from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 1 — DFS + set  (my approach, store complement first)
#
# For each node store k - node.val in the set before visiting children.
# When we later visit a node whose value is already in the set, a pair exists.
#
# Order: check → store complement → recurse left → recurse right
# Time: O(n)   Space: O(n)
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def findTarget_v1(self, root, k):
        self.k    = k
        self.diff = set()

        def pair(curr):
            if not curr:
                return False
            if curr.val in self.diff:       # complement was stored earlier
                return True
            self.diff.add(k - curr.val)     # store what we'd need to pair with curr
            return pair(curr.left) or pair(curr.right)

        return pair(root)


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 2 — DFS + set  (cleaner version, store visited values)
#
# Store each visited node's value in `seen`.
# When we arrive at a node, check if its complement (k - val) is already seen.
#
# Order: check → store curr.val → recurse
# Time: O(n)   Space: O(n)
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def findTarget_v2(self, root, k):
        seen = set()

        def f(node):
            if not node:
                return False
            if k - node.val in seen:        # complement already visited
                return True
            seen.add(node.val)
            return f(node.left) or f(node.right)

        return f(root)


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 3 — inorder → sorted list → two pointers
#
# Inorder traversal of a BST gives a sorted array.
# Classic two-sum on a sorted array: lo pointer from the left,
# hi pointer from the right, converge until they meet.
# Time: O(n)   Space: O(n)
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def findTarget(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: bool
        """
        # build sorted list via inorder
        nums = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            nums.append(node.val)
            inorder(node.right)

        inorder(root)

        # two-pointer two-sum on sorted array
        lo, hi = 0, len(nums) - 1
        while lo < hi:
            s = nums[lo] + nums[hi]
            if s == k:
                return True
            elif s < k:
                lo += 1
            else:
                hi -= 1

        return False


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


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([5, 3, 6, 2, 4, None, 7], 9,  True),
        ([5, 3, 6, 2, 4, None, 7], 28, False),
        ([2, 1, 3],                 4,  True),   # 1+3
        ([2, 1, 3],                 1,  False),  # no pair sums to 1
        ([1],                       2,  False),  # single node, can't pair with itself
    ]

    for values, k, expected in test_cases:
        tree = buildTree(values)
        result = sol.findTarget(tree, k)
        status = "✅" if result == expected else "❌"
        print(f"{status}  k={k}, tree={values} → {result}  (expected {expected})")
