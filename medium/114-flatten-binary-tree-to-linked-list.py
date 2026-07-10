from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ❌ Attempt — O(1) space Morris-like, but wrong order of operations
#
# BUG: `saved_left = curr.left` was written AFTER `curr.left = None`.
# So saved_left was always None, and `curr = saved_left` skipped the
# entire left subtree → output was [1,null,5,null,6] instead of
# [1,null,2,null,3,null,4,null,5,null,6].
#
# FIX: save the left child BEFORE nulling it.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def flatten_attempt(self, root):
        curr = root
        while curr:
            if curr.left is None:
                curr = curr.right
            else:
                pred = curr.left
                while pred.right:
                    pred = pred.right

                # ✅ save BEFORE nulling
                saved_left = curr.left          # ← must come first
                curr.left = None                # ← then null

                pred.right = curr.right         # wire old right onto pred
                curr.right = saved_left         # plug left subtree as new right
                curr = curr.right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 1 — O(1) space, in-place (follow-up answer)
#
# For each node that has a left child:
#   1. Find the rightmost node of the LEFT subtree (it will come just
#      before curr.right in preorder order).
#   2. Wire that node's right pointer to curr's right subtree.
#   3. Move the left subtree to curr's right.
#   4. Null curr's left.
#   5. Advance right.
#
# No thread to remove — we're permanently rewiring, not temporarily.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def flatten(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: None  Do not return anything, modify root in-place instead.
        """
        curr = root
        while curr:
            if curr.left:
                # find rightmost of left subtree
                pred = curr.left
                while pred.right:
                    pred = pred.right

                pred.right = curr.right     # attach curr's right subtree at the end
                curr.right = curr.left      # left subtree becomes new right
                curr.left = None            # clear left

            curr = curr.right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 2 — recursive (reverse postorder: right → left → root)
#
# Process right then left subtree first, keeping track of the previously
# flattened node (`prev`). Attach prev as the right child of current root.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def flatten(self, root):
        self.prev = None

        def dfs(node):
            if not node:
                return
            dfs(node.right)
            dfs(node.left)
            node.right = self.prev
            node.left = None
            self.prev = node

        dfs(root)


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 3 — iterative with stack (explicit preorder)
#
# Preorder using a stack; build the list by wiring right pointers as we pop.
# O(n) time, O(n) space (stack).
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def flatten(self, root):
        if not root:
            return
        stack = [root]
        prev = None
        while stack:
            node = stack.pop()
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
            if prev:
                prev.right = node
                prev.left = None
            prev = node
        prev.left = None


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


def flatToList(root):
    res = []
    while root:
        res.append(root.val)
        assert root.left is None, "left pointer not null!"
        root = root.right
    return res


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([1, 2, 5, 3, 4, None, 6], [1, 2, 3, 4, 5, 6]),
        ([],                        []),
        ([0],                       [0]),
    ]

    for i, (input_list, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        sol.flatten(root)
        output = flatToList(root) if root else []
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
