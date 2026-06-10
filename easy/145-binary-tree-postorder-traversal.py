from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Recursive solution
class Solution(object):
    def postorderTraversal(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: List[int]
        """
        if not root:
            return []

        def postOrder(root, res):
            if root.left: postOrder(root.left, res)
            if root.right: postOrder(root.right, res)
            res.append(root.val)

        res = []
        postOrder(root, res)
        return res


# Iterative solution (follow-up)
# Postorder (left→right→root) is the reverse of a modified preorder (root→right→left).
# Push left before right so right is popped first, then reverse the collected result.
class Solution(object):
    def postorderTraversal(self, root):
        if not root:
            return []

        res, stack = [], [root]

        while stack:
            node = stack.pop()
            res.append(node.val)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

        return res[::-1]


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
    sol = Solution()

    test_cases = [
        ([1, None, 2, 3], [3, 2, 1]),
        ([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9], [4, 6, 7, 5, 2, 9, 8, 3, 1]),
        ([], []),
        ([1], [1]),
    ]

    for i, (input_list, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        output = sol.postorderTraversal(root)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
