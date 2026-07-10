from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 1 (mine) — findParent helper, then attach
#
# Walk the tree to find the insertion point, tracking both the last visited
# node (parent) and the direction we last went (l/r). Then attach the new
# node as parent.left or parent.right accordingly.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def insertIntoBST_v1(self, root, val):
        if not root:
            return TreeNode(val)

        def findParent(root, val):
            direction = "l"
            curr = parent = root
            while curr:
                parent = curr
                if curr.val < val:
                    direction = "r"
                    curr = curr.right
                else:
                    direction = "l"
                    curr = curr.left
            return [parent, direction]

        parent, direction = findParent(root, val)
        if direction == "l":
            parent.left = TreeNode(val)
        else:
            parent.right = TreeNode(val)

        return root


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 2 — cleaner iterative, no direction tracking needed
#
# Check for a free child slot as we walk. The moment we find curr.left/right
# is None in the correct direction, insert there and break.
# Eliminates the separate direction variable — the check is done in-line.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def insertIntoBST(self, root, val):
        """
        :type root: Optional[TreeNode]
        :type val: int
        :rtype: Optional[TreeNode]
        """
        if not root:
            return TreeNode(val)

        curr = root
        while curr:
            if val < curr.val:
                if curr.left is None:
                    curr.left = TreeNode(val)
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = TreeNode(val)
                    break
                curr = curr.right

        return root


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 3 — recursive (concise)
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def insertIntoBST(self, root, val):
        if not root:
            return TreeNode(val)
        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        else:
            root.right = self.insertIntoBST(root.right, val)
        return root


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


# ✅ Tester
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([4, 2, 7, 1, 3],                      5,  [4, 2, 7, 1, 3, 5]),
        ([40, 20, 60, 10, 30, 50, 70],         25,  [40, 20, 60, 10, 30, 50, 70, None, None, 25]),
        ([4, 2, 7, 1, 3, None, None],           5,  [4, 2, 7, 1, 3, 5]),
        ([],                                    5,  [5]),
    ]

    for i, (input_list, val, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        result = sol.insertIntoBST(root, val)
        output = levelOrder(result)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input: {input_list}, val={val}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
