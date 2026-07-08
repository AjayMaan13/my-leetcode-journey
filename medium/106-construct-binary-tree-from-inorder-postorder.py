from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ✅ Optimised — O(n) time, no slicing
#
# Mirror of problem 105 (preorder + inorder), with two key differences:
#
#   DIFFERENCE 1: Root comes from the END of postorder, not the start.
#     Postorder = left → right → root, so reading backwards gives root → right → left.
#     Pointer starts at len(postorder) - 1 and DECREMENTS each call.
#
#   DIFFERENCE 2: Right subtree must be built BEFORE left.
#     Because we consume postorder in reverse (root, then right subtree roots,
#     then left subtree roots), we must recurse right first so the pointer
#     lines up correctly — the opposite of problem 105.
#
#   Everything else is identical:
#     - idx_map {val: index} for O(1) inorder lookup (replaces O(n) .index())
#     - (left, right) boundaries instead of slicing inorder copies
class Solution(object):
    def buildTree(self, inorder, postorder):
        """
        :type inorder: List[int]
        :type postorder: List[int]
        :rtype: Optional[TreeNode]
        """
        idx_map = {val: i for i, val in enumerate(inorder)}
        self.post_idx = len(postorder) - 1

        def findBT(left, right):
            if left > right:
                return None

            root = postorder[self.post_idx]
            self.post_idx -= 1

            node = TreeNode(root)
            i = idx_map[root]

            # Right MUST come before left — mirrors postorder's right→left (read backwards)
            node.right = findBT(i + 1, right)
            node.left  = findBT(left,  i - 1)

            return node

        return findBT(0, len(inorder) - 1)


# ✅ Build tree from list (level order) — for test comparison
def buildFromList(values):
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
        if node:
            res.append(node.val)
            q.append(node.left)
            q.append(node.right)
        else:
            res.append(None)
    while res and res[-1] is None:
        res.pop()
    return res


# ✅ Tester
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([9, 3, 15, 20, 7], [9, 15, 7, 20, 3], [3, 9, 20, None, None, 15, 7]),
        ([-1], [-1], [-1]),
    ]

    for i, (inorder, postorder, expected_list) in enumerate(test_cases, 1):
        root = sol.buildTree(inorder, postorder)
        output   = levelOrder(root)
        expected = levelOrder(buildFromList(expected_list))
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Inorder:   {inorder}")
        print(f"  Postorder: {postorder}")
        print(f"  Expected:  {expected}")
        print(f"  Got:       {output}\n")
