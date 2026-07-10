from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 1 — DFS preorder (serialize: root,left,right; nulls as "N")
#
# serialize: preorder DFS, append node value or "N" for null.
#   Join with "," → "1,2,N,N,3,4,N,N,5,N,N"
#
# deserialize: split on ",", use a pointer self.i to consume tokens left-to-right.
#   "N" → return None (base case)
#   Otherwise → build node, recurse left then right.
#
# Note: the `root.left = dfs(root.left)` lines in serialize are unnecessary
# assignments (dfs returns None), but since we only care about `result`,
# the serialized string is still correct.
# ─────────────────────────────────────────────────────────────────────────────
class Codec:
    def serialize(self, root):
        """
        :type root: TreeNode
        :rtype: str
        """
        result = []

        def dfs(node):
            if not node:
                result.append("N")
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(result)

    def deserialize(self, data):
        """
        :type data: str
        :rtype: TreeNode
        """
        vals = data.split(",")
        self.i = 0

        def dfs():
            if vals[self.i] == "N":
                self.i += 1
                return None
            node = TreeNode(int(vals[self.i]))
            self.i += 1
            node.left  = dfs()
            node.right = dfs()
            return node

        return dfs()


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 2 — BFS level-order (serialize level by level; nulls as "#")
#
# serialize: BFS, enqueue even null children so we can reconstruct structure.
#   "#" marks a null node.
#   Example tree [1,2,3,null,null,4,5] → "1,2,3,#,#,4,5,#,#,#,#"
#
# deserialize: split on ",", first token is root, then use a BFS queue.
#   For each non-null node popped from queue, consume next two tokens as
#   its left and right children (creating nodes only if token != "#").
# ─────────────────────────────────────────────────────────────────────────────
class Codec:
    def serialize(self, root):
        if root is None:
            return "#"

        vals = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                vals.append("#")
            else:
                vals.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)

        return ",".join(vals)

    def deserialize(self, data):
        vals = data.split(",")
        if vals[0] == "#":
            return None

        root = TreeNode(int(vals[0]))
        queue = deque([root])
        i = 1

        while queue:
            node = queue.popleft()

            left_val = vals[i]; i += 1
            if left_val != "#":
                node.left = TreeNode(int(left_val))
                queue.append(node.left)

            right_val = vals[i]; i += 1
            if right_val != "#":
                node.right = TreeNode(int(right_val))
                queue.append(node.right)

        return root


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
    codec = Codec()

    test_cases = [
        [1, 2, 3, None, None, 4, 5],
        [],
        [1],
        [1, 2],
    ]

    for input_list in test_cases:
        original = buildTree(input_list)
        serialized = codec.serialize(original)
        restored = codec.deserialize(serialized)
        out = levelOrder(restored)
        exp = levelOrder(buildTree(input_list))
        status = "✅ Passed" if out == exp else "❌ Failed"
        print(f"{status}  Input: {input_list}")
        print(f"        Serialized: {serialized}")
        print(f"        Restored:   {out}\n")
