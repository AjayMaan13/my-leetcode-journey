"""
LeetCode Problem: 1008. Construct Binary Search Tree from Preorder Traversal
Link: https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/

Description:
Given an array representing the preorder traversal of a BST, reconstruct and return the root.

Example:
preorder = [8, 5, 1, 7, 10, 12]

Preorder means: root first, then left subtree, then right subtree.
In a BST: left subtree values < root < right subtree values.

So 8 is root. Everything < 8 (→ 5,1,7) goes left; everything > 8 (→ 10,12) goes right.

Reconstructed tree:
         8
        / \\
       5   10
      / \\    \\
     1   7   12

Output: [8, 5, 10, 1, 7, null, 12]
"""

from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 1 — naive BST insertion  O(n²) worst case / O(n log n) avg
#
# The simplest approach: treat preorder as a sequence of insertions.
# Because preorder visits root before children, inserting left-to-right
# naturally rebuilds the original BST (root goes in first, then its subtrees).
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def bstFromPreorder_v1(self, preorder):
        def insert(root, val):
            if not root:
                return TreeNode(val)
            if val < root.val:
                root.left = insert(root.left, val)
            else:
                root.right = insert(root.right, val)
            return root

        root = None
        for val in preorder:
            root = insert(root, val)
        return root


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 2 — bound-based recursive  O(n) time  O(h) space  ← submitted
#
# Key insight: in preorder, each node's LEFT subtree can only contain values
# strictly less than that node's own value. So pass a `bound` (upper limit)
# down: stop recursing when the next preorder value exceeds the bound.
#
# Walk:
#   bst(inf)            → reads 8, left=bst(8),  right=bst(inf)
#     bst(8)            → reads 5, left=bst(5),  right=bst(8)
#       bst(5)          → reads 1, left=bst(1),  right=bst(5)
#         bst(1)        → reads 7, 7 >= 1 bound? No... wait, bound=1 here?
#
# More precisely:
#   node.left  = bst(val)   ← left subtree: values must be < val
#   node.right = bst(bound) ← right subtree: values must be < parent's bound
#
# The self.idx pointer advances only when we actually consume a node
# (i.e. when the value passes the bound check). No slicing needed.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def bstFromPreorder_v2(self, preorder):
        self.preorder = preorder
        self.idx = 0

        def bst(bound):
            # No more values, or next value doesn't belong in this subtree
            if self.idx == len(self.preorder) or self.preorder[self.idx] >= bound:
                return None

            val = self.preorder[self.idx]
            self.idx += 1
            node = TreeNode(val)
            node.left  = bst(val)    # left children must be < current val
            node.right = bst(bound)  # right children must be < inherited bound
            return node

        return bst(float("inf"))


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 3 — iterative with stack  O(n) time  O(h) space
#
# Maintain a stack representing the "path from root to the last inserted node"
# (the right-spine of nodes still waiting for a right child).
#
# For each new value v:
#   - If v < stack[-1].val  → v is the LEFT child of the stack top
#     (in preorder, the left child always comes immediately after its parent)
#   - If v > stack[-1].val  → pop nodes until we find a node where v < that node.
#     v becomes the RIGHT child of the last popped node (the deepest ancestor
#     whose bound v still satisfies).
#
# The stack always shrinks as we commit right children; newly added nodes push.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def bstFromPreorder(self, preorder):
        """
        :type preorder: List[int]
        :rtype: Optional[TreeNode]
        """
        root = TreeNode(preorder[0])
        stack = [root]

        for val in preorder[1:]:
            node = TreeNode(val)

            if val < stack[-1].val:
                # Smaller than top → must be its left child
                stack[-1].left = node
            else:
                # Larger → pop until we find the correct parent for the right side
                parent = None
                while stack and stack[-1].val < val:
                    parent = stack.pop()
                parent.right = node

            stack.append(node)  # this node may still get a right child later

        return root


# ─────────────────────────────────────────────────────────────────────────────
# Helpers for testing
# ─────────────────────────────────────────────────────────────────────────────
def levelOrder(root):
    if not root:
        return []
    q, res = deque([root]), []
    while q:
        node = q.popleft()
        res.append(node.val if node else None)
        if node:
            q.append(node.left)
            q.append(node.right)
    while res and res[-1] is None:
        res.pop()
    return res


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([8, 5, 1, 7, 10, 12], [8, 5, 10, 1, 7, None, 12]),
        ([1, 3],                [1, None, 3]),
        ([5],                   [5]),
        ([3, 1, 2],             [3, 1, None, None, 2]),
    ]

    for preorder, expected in test_cases:
        result = sol.bstFromPreorder(preorder)
        output = levelOrder(result)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"{status}  preorder={preorder}")
        print(f"         expected={expected}")
        print(f"         got     ={output}\n")
