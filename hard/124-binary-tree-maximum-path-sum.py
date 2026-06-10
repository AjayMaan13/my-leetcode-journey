from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# DFS: for each node, the best path through it is node.val + max(left gain, 0) + max(right gain, 0).
# To contribute to a parent, only one branch can be extended — return node.val + max single branch.
class Solution(object):
    def maxPathSum(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        self.maxSum = root.val

        def dfs(node):
            if not node:
                return 0
            left = max(0, dfs(node.left))
            right = max(0, dfs(node.right))
            self.maxSum = max(self.maxSum, node.val + left + right)
            return node.val + max(left, right)

        dfs(root)
        return self.maxSum


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
        ([1, 2, 3], 6),
        ([-10, 9, 20, None, None, 15, 7], 42),
        ([-3], -3),
    ]

    for i, (input_list, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        output = sol.maxPathSum(root)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
