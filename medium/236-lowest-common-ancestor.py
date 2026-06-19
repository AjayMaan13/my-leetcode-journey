from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# ─────────────────────────────────────────────────────────────────────────────
# ❌ Attempt 1 — path-finding approach (too complex, edge cases fail)
#
# Idea: find path root→p and root→q separately, then compare.
# Problem: the LCA logic at the end is fragile (returns a value, not a node)
# and the dfs inner logic was never completed correctly.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def lowestCommonAncestor_v1(self, root, p, q):
        if not root or not p or not q:
            return None

        path = []

        def dfs(node, target):
            if not node:
                return False
            path.append(node.val)
            if node.val == target:
                return True
            if dfs(node.left, target) or dfs(node.right, target):
                return True
            path.pop()
            return False

        dfs(root, p.val)
        pPath = path[::]
        path.clear()

        dfs(root, q.val)
        qPath = path[::]

        # Walk both paths until they diverge — last common node is the LCA
        lca = None
        for a, b in zip(pPath, qPath):
            if a == b:
                lca = a
            else:
                break
        return lca


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Attempt 2 — standard recursive LCA (what LeetCode expects)
#
# 🧠 The "signal" intuition vs this solution:
#
#   You were imagining a label system:
#       return 1  →  found p
#       return 2  →  found q
#       return 3  →  found both (LCA here)
#
#   That idea is valid, but LCA doesn't actually need to distinguish p vs q.
#   It only needs to know: "did I find SOMETHING from below?"
#
#   So instead of labels 1 / 2, we use:
#       return node p    (truthy — something found)
#       return node q    (truthy — something found)
#       return None      (falsy — nothing found)
#
#   The "both sides non-null" check replaces your label-3 case:
#       if left and right: → this IS the LCA node (split point)
#
#   Mapping your idea → this solution:
#       Your "return 1 (p)"   →  return node p
#       Your "return 2 (q)"   →  return node q
#       Your "return 3 (both)"→  handled by `if left and right: return root`
#
# 🔑 Key insight:
#   You were building a label system to track WHICH node was found.
#   LCA only needs to track WHETHER something was found.
#   "node or None" is simpler and carries enough information.
#
# 🔥 Mental model:
#   Instead of: "I should tag p and q differently"
#   Think:      "I only care if something exists below me, not what it is"
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        if not root:
            return None

        # If we reach p or q, signal its presence upward
        if root == p or root == q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # Both sides returned something → this node is the split point = LCA
        if left and right:
            return root

        # Only one side found something → bubble it up
        return left if left else right


# ✅ Build tree from list (level order)
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


# ✅ Tester
if __name__ == "__main__":
    # Tree: [3,5,1,6,2,0,8,null,null,7,4]
    root = TreeNode(3)
    root.left = TreeNode(5)
    root.right = TreeNode(1)
    root.left.left = TreeNode(6)
    root.left.right = TreeNode(2)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(8)
    root.left.right.left = TreeNode(7)
    root.left.right.right = TreeNode(4)

    sol = Solution()

    p, q = root.left, root.right          # 5, 1  → LCA = 3
    print(sol.lowestCommonAncestor(root, p, q).val)  # Expected: 3

    p, q = root.left, root.left.right.right  # 5, 4 → LCA = 5
    print(sol.lowestCommonAncestor(root, p, q).val)  # Expected: 5
