from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Recursive solution
class Solution(object):
    def inorderTraversal(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: List[int]
        """
        if not root:
            return []

        def inOrder(root, res):
            if root.left: inOrder(root.left, res)
            res.append(root.val)
            if root.right: inOrder(root.right, res)

        res = []
        inOrder(root, res)
        return res


# Iterative solution (follow-up)
# Use an explicit stack to simulate the call stack of the recursive approach.
# Go as far left as possible, then process, then move right.
class Solution(object):
    def inorderTraversal(self, root):
        res, stack = [], []
        curr = root

        while curr or stack:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            res.append(curr.val)
            curr = curr.right

        return res


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
        ([1, None, 2, 3], [1, 3, 2]),
        ([1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9], [4, 2, 6, 5, 7, 1, 3, 9, 8]),
        ([], []),
        ([1], [1]),
    ]

    for i, (input_list, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        output = sol.inorderTraversal(root)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
