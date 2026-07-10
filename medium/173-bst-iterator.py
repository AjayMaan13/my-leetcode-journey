"""
LeetCode Problem: 173. Binary Search Tree Iterator
Link: https://leetcode.com/problems/binary-search-tree-iterator/

Description:
Implement BSTIterator over the inorder traversal of a BST:
  __init__(root) — initialise; pointer starts before the smallest element
  next()         — move pointer right, return the value (always valid to call)
  hasNext()      — True if there is a value to the right of the pointer

Follow-up: Can you implement next() and hasNext() in average O(1) time
           and O(h) memory, where h is the height of the tree?

Example:
  Tree: [7, 3, 15, null, null, 9, 20]
         7
        / \\
       3   15
          /  \\
         9   20

  Calls:
    next()    → 3
    next()    → 7
    hasNext() → True
    next()    → 9
    hasNext() → True
    next()    → 15
    hasNext() → True
    next()    → 20
    hasNext() → False
"""

from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 1 — brute force: precompute full inorder list
#
# Build the entire sorted list once in __init__.
# next() and hasNext() are O(1), but uses O(n) memory — violates follow-up.
# ─────────────────────────────────────────────────────────────────────────────
class BSTIterator_v1(object):
    def __init__(self, root):
        self._vals = []
        self._idx  = 0
        self._build(root)

    def _build(self, node):
        if not node:
            return
        self._build(node.left)
        self._vals.append(node.val)
        self._build(node.right)

    def next(self):
        val = self._vals[self._idx]
        self._idx += 1
        return val

    def hasNext(self):
        return self._idx < len(self._vals)


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 2 — lazy stack (satisfies the follow-up)
#
# Key idea: the standard iterative inorder keeps a stack of the "left spine"
# of nodes not yet visited. We freeze that state between method calls instead
# of running the whole traversal at once.
#
# _push_left(node): push node and all its left descendants — these are the
#   next candidates in ascending order.
#
# next():
#   1. Pop stack top — smallest remaining node.
#   2. Push its right child's left spine — prepares the next candidates.
#   3. Return the popped value.
#
# hasNext(): stack non-empty → more nodes to visit.
#
# Time: __init__ O(h), each next() amortised O(1)  (every node pushed once, popped once)
# Space: O(h)  — stack holds at most one root-to-leaf path at a time
# ─────────────────────────────────────────────────────────────────────────────
class BSTIterator(object):
    def __init__(self, root):
        """
        :type root: Optional[TreeNode]
        """
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        """
        :rtype: int
        """
        node = self.stack.pop()         # smallest remaining node
        self._push_left(node.right)     # prepare the next portion of inorder
        return node.val

    def hasNext(self):
        """
        :rtype: bool
        """
        return len(self.stack) > 0


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
    tree = buildTree([7, 3, 15, None, None, 9, 20])

    for cls_name, cls in [("v1 brute", BSTIterator_v1), ("v2 lazy stack", BSTIterator)]:
        it = cls(tree)
        results = []
        while it.hasNext():
            results.append(it.next())
        expected = [3, 7, 9, 15, 20]
        status = "✅" if results == expected else "❌"
        print(f"{status} {cls_name}: {results}  (expected {expected})")
