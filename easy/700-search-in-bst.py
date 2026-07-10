from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Recursive — exploits BST property: go left if val < root, right if val > root
class Solution(object):
    def searchBST(self, root, val):
        """
        :type root: Optional[TreeNode]
        :type val: int
        :rtype: Optional[TreeNode]
        """
        if not root:
            return None
        if root.val == val:
            return root
        elif root.val > val:
            return self.searchBST(root.left, val)
        else:
            return self.searchBST(root.right, val)


# Iterative — same logic, O(1) space (no call stack)
class Solution(object):
    def searchBST(self, root, val):
        curr = root
        while curr:
            if curr.val == val:
                return curr
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return None


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

    tree = buildTree([4, 2, 7, 1, 3])

    test_cases = [
        (tree, 2, [2, 1, 3]),
        (tree, 5, []),
    ]

    for i, (root, val, expected) in enumerate(test_cases, 1):
        result = sol.searchBST(root, val)
        output = levelOrder(result)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  val={val}, Expected: {expected}, Got: {output}\n")
