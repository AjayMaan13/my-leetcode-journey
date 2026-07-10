"""
⭐ IMPORTANT REVISION — BST Iterator  (LeetCode 173 · Medium)
--------------------------------------------------------------
Full solution: medium/173-bst-iterator.py

Why it's important:
  The "push left spine onto a stack" pattern is the building block for
  several BST problems. Internalising it once unlocks all of them:

  ┌──────────────────────────────────────┬─────────────────────────────┐
  │ Problem                              │ How iterator pattern applies │
  ├──────────────────────────────────────┼─────────────────────────────┤
  │ 230. Kth Smallest in BST             │ pop k-th element from stack  │
  │ 98.  Validate BST                    │ check prev < curr on pop     │
  │ 173. BST Iterator (this)             │ expose pop as next() method  │
  │ Merge Two BSTs (Extra/bst/04)        │ two iterators merged on-fly  │
  │ Predecessor & Successor (Extra/bst/02)│ iterator + stop condition   │
  └──────────────────────────────────────┴─────────────────────────────┘

Core pattern (memorise this):
─────────────────────────────
  stack = []

  def push_left(node):          # push current node + its entire left spine
      while node:
          stack.append(node)
          node = node.left

  def next():
      node = stack.pop()        # smallest remaining
      push_left(node.right)     # expose right subtree's left spine
      return node.val

  def has_next():
      return bool(stack)

Why O(h) space:
  The stack holds exactly one root-to-leaf path at any moment.
  The longest path is h (tree height). For a balanced BST h = log n,
  so this is much better than the O(n) brute-force precomputed list.

Why amortised O(1) per next():
  Every node is pushed exactly once and popped exactly once across all
  next() calls, giving O(n) total work across n calls → O(1) amortised.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# Core pattern — commit this to memory
# ─────────────────────────────────────────────────────────────────────────────
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self):
        return bool(self.stack)


# ─────────────────────────────────────────────────────────────────────────────
# Quick self-test
# ─────────────────────────────────────────────────────────────────────────────
def buildTree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i]); q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]); q.append(node.right)
        i += 1
    return root


if __name__ == "__main__":
    it = BSTIterator(buildTree([7, 3, 15, None, None, 9, 20]))
    result = []
    while it.hasNext():
        result.append(it.next())
    print("✅" if result == [3, 7, 9, 15, 20] else "❌", result)
