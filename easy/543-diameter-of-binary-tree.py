from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# DFS: at each node the diameter candidate is left_height + right_height (edges through this node).
# Track the global max via self.diameter while computing heights bottom-up.
class Solution(object):
    def diameterOfBinaryTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        self.diameter = 0

        def height(node):
            if not node:
                return 0
            left = height(node.left)
            right = height(node.right)
            self.diameter = max(self.diameter, left + right)
            return 1 + max(left, right)

        height(root)
        return self.diameter


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
        ([1, 2, 3, 4, 5], 3),
        ([1, 2], 1),
        ([1], 0),
    ]

    for i, (input_list, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        output = sol.diameterOfBinaryTree(root)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
