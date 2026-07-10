"""
BST Iterator  (IMP)
--------------------
LeetCode 173 — Medium

Implement BSTIterator over the inorder traversal of a BST:
  __init__(root) — initialise; pointer starts before the smallest element
  next()         — advance pointer, return the value (always valid to call)
  hasNext()      — True if there is still a value to the right of the pointer

Example:
         7
        / \\
       3   15
          /  \\
         9   20

Calls:  next()→3, next()→7, hasNext()→True,
        next()→9, hasNext()→True, next()→15,
        hasNext()→True, next()→20, hasNext()→False

─────────────────────────────────────────────────────────────────────────────
WHY THIS IS IMPORTANT
─────────────────────────────────────────────────────────────────────────────
The follow-up asks for:
  • next() / hasNext() in *average* O(1) time
  • O(h) memory  (h = height, NOT O(n))

Precomputing the full inorder list gives O(1) per call but uses O(n) memory.
The stack-based lazy approach satisfies BOTH constraints — and the same
"push-left spine" helper appears in kthSmallest, validateBST, and many other
iterative inorder problems. Internalising this pattern is the payoff.
"""

from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 1 — brute force: precompute full inorder list
#
# Build the entire sorted list in __init__, then serve values by index.
# next() and hasNext() are O(1), but __init__ is O(n) time AND O(n) space.
# Violates the O(h) memory constraint in the follow-up.
# ─────────────────────────────────────────────────────────────────────────────
class BSTIterator_v1:
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
# ✅ Approach 2 — lazy stack-based  ← submitted, satisfies the follow-up
#
# Intuition: standard iterative inorder uses a stack holding the "left spine"
# of the current position. We freeze that state between calls instead of
# running the whole traversal at once.
#
# _push_left(node): push every node from `node` down its left spine.
#   This represents "I haven't visited these yet, but they're next in order."
#
# next():
#   1. Pop the stack top — that's the next inorder node.
#   2. Push its RIGHT child's left spine (the next candidates after this node).
#   3. Return the popped value.
#
# hasNext(): stack is non-empty ↔ there are still nodes to visit.
#
# Time: O(h) for __init__; amortized O(1) per next() call
#       (each node is pushed and popped exactly once across all calls)
# Space: O(h) — the stack holds at most one root-to-leaf path
# ─────────────────────────────────────────────────────────────────────────────
class BSTIterator:
    def __init__(self, root):
        """
        :type root: Optional[TreeNode]
        """
        self.stack = []
        self._push_left(root)           # prime the stack with the left spine of root

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        """
        :rtype: int
        """
        node = self.stack.pop()         # smallest remaining node
        self._push_left(node.right)     # prepare the left spine of the right subtree
        return node.val

    def hasNext(self):
        """
        :rtype: bool
        """
        return len(self.stack) > 0


# ─────────────────────────────────────────────────────────────────────────────
# Connection to kthSmallest (230):
#
#   The iterative inorder in kthSmallest does:
#       while stack or curr:
#           while curr: stack.append(curr); curr = curr.left
#           curr = stack.pop()
#           k -= 1; if k == 0: return curr.val
#           curr = curr.right
#
#   BSTIterator is that same loop split across method calls:
#       __init__  → first "while curr: push left"
#       next()    → pop + push right's left spine (one iteration of the outer loop)
#
#   Same stack, same invariant — just exposed as an object instead of a loop.
# ─────────────────────────────────────────────────────────────────────────────


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
        print(f"{status} {cls_name}: {results}")

    # Simulate the exact LeetCode call sequence
    print("\n── LeetCode sequence ──")
    it = BSTIterator(tree)
    calls = [
        ("next",    None, 3),
        ("next",    None, 7),
        ("hasNext", None, True),
        ("next",    None, 9),
        ("hasNext", None, True),
        ("next",    None, 15),
        ("hasNext", None, True),
        ("next",    None, 20),
        ("hasNext", None, False),
    ]
    for method, _, expected in calls:
        result = it.next() if method == "next" else it.hasNext()
        status = "✅" if result == expected else "❌"
        print(f"  {status} {method}() → {result}  (expected {expected})")
