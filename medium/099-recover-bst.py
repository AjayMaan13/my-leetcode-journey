"""
LeetCode Problem: 99. Recover Binary Search Tree
Link: https://leetcode.com/problems/recover-binary-search-tree/

Description:
Exactly two nodes of a BST were swapped by mistake.
Recover the tree without changing its structure (swap their values back).

Follow-up: O(n) space is straightforward. Can you do O(1) space?

Key insight:
  Inorder traversal of a valid BST produces a strictly increasing sequence.
  Two swapped nodes create exactly 1 or 2 "violations" (places where prev > curr).

  Case 1 — adjacent swap (e.g. [1,3,null,null,2] swapped 1↔3 which are neighbours):
    Only ONE violation: prev=3 > curr=1
    → first=3 (prev at violation), second=1 (curr at violation)

  Case 2 — non-adjacent swap (e.g. [3,1,4,null,null,2] swapped 2↔3):
    TWO violations: prev=3>curr=2 then later prev=3>curr=2 ...
    Actually: inorder is [1,3,2,4] → violation at 3>2
    For [6,2,8,…] with 2 and 8 swapped → [8,…,2,…] → violation at 8>x (first=8)
    and second violation later where prev>curr (second=curr)

    Always update second=curr at EVERY violation.
    Only set first=prev at the FIRST violation.
    This handles both cases:
      - 1 violation: first=prev, second=curr  (adjacent)
      - 2 violations: first=prev₁ (first violation), second=curr₂ (second violation)

Example 1: root=[1,3,null,null,2]
  Inorder: 3 → 2 → 1  →  violation at 3>2: first=3,second=2
                          violation at 2>1: second=1  (first stays 3)
  Swap 3.val ↔ 1.val → [3,1,null,null,2] ✓   wait...

  Actually inorder of [1,3,null,null,2]:
       1
      /
     3
      \\
       2
  Inorder: 3,2,1 → two violations; first=3, second=1; swap → correct tree

Example 2: root=[3,1,4,null,null,2]
       3
      / \\
     1   4
        /
       2
  Inorder: 1,3,2,4 → one violation (3>2); first=3, second=2; swap → [2,1,4,null,null,3] ✓
"""

from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 1 — iterative inorder with explicit stack  O(n) time, O(h) space
#                                                        ← submitted
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def recoverTree_v1(self, root):
        stack       = []
        curr        = root
        first       = None
        second      = None
        lastVisited = TreeNode(float("-inf"))

        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left

            curr = stack.pop()

            if curr.val < lastVisited.val:
                if first is None:
                    first = lastVisited   # larger node out of place (first violation)
                second = curr             # always update: smaller node out of place

            lastVisited = curr
            curr = curr.right

        first.val, second.val = second.val, first.val


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 2 — recursive inorder  O(n) time, O(h) space (call stack)
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def recoverTree_v2(self, root):
        self.first  = None
        self.second = None
        self.prev   = TreeNode(float('-inf'))

        def inorder(node):
            if not node:
                return
            inorder(node.left)

            # violation: previous inorder value is larger than current
            if self.prev.val > node.val:
                if not self.first:
                    self.first = self.prev  # first violation → prev is the culprit
                self.second = node          # always update second (handles both cases)

            self.prev = node
            inorder(node.right)

        inorder(root)
        self.first.val, self.second.val = self.second.val, self.first.val


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 3 — Morris inorder  O(n) time, O(1) space  ← answers the follow-up
#
# Same logic as solutions 1/2 but uses threaded predecessor pointers instead
# of a stack or recursion. We visit each node exactly twice (thread + unthread),
# so the inorder visit happens when we unthread (pred.right == curr).
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def recoverTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: None  (modify root in-place)
        """
        first  = None
        second = None
        prev   = TreeNode(float('-inf'))
        curr   = root

        while curr:
            if curr.left is None:
                # no left subtree → this is the real inorder visit
                if prev.val > curr.val:
                    if not first:
                        first = prev
                    second = curr
                prev = curr
                curr = curr.right

            else:
                # find inorder predecessor
                pred = curr.left
                while pred.right and pred.right != curr:
                    pred = pred.right

                if pred.right is None:
                    pred.right = curr       # thread: come back after left subtree
                    curr = curr.left
                else:
                    pred.right = None       # unthread: left subtree done → visit curr
                    if prev.val > curr.val:
                        if not first:
                            first = prev
                        second = curr
                    prev = curr
                    curr = curr.right

        first.val, second.val = second.val, first.val


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


def inorderList(root):
    res = []
    def dfs(node):
        if not node: return
        dfs(node.left); res.append(node.val); dfs(node.right)
    dfs(root)
    return res


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 3, None, None, 2], [1, 2, 3]),   # adjacent swap
        ([3, 1, 4, None, None, 2], [1, 2, 3, 4]),  # non-adjacent swap
        ([2, 3, 1], [1, 2, 3]),
    ]

    for values, expected_inorder in test_cases:
        tree = buildTree(values)
        sol.recoverTree(tree)
        result = inorderList(tree)
        status = "✅" if result == expected_inorder else "❌"
        print(f"{status}  input={values} → inorder after fix: {result}  (expected {expected_inorder})")
