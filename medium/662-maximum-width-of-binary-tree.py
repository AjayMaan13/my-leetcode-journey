from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Solution 1 — compare first and last positions in the queue directly
# Width at each level = last_pos - first_pos + 1.
# Check only when the level has >1 node (queue[0] != queue[-1]).
class Solution(object):
    def widthOfBinaryTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        if not root:
            return 0

        queue = deque([[root, 1]])
        maxWidth = 1

        while queue:
            length = len(queue)
            if queue[0] != queue[-1]:
                maxWidth = max(queue[-1][1] - queue[0][1] + 1, maxWidth)
            for _ in range(length):
                node, pos = queue.popleft()
                if node.left:
                    queue.append([node.left, pos * 2])
                if node.right:
                    queue.append([node.right, pos * 2 + 1])

        return maxWidth


# Solution 2 — cleaner: snapshot first_pos at level start, last_pos at level end
# Indexes from 0 (avoids off-by-one on the initial push).
class Solution(object):
    def widthOfBinaryTree(self, root):
        if not root:
            return 0

        queue = deque([(root, 0)])
        maxWidth = 1

        while queue:
            level_size = len(queue)
            _, first_pos = queue[0]

            for i in range(level_size):
                node, pos = queue.popleft()
                if i == level_size - 1:
                    last_pos = pos
                if node.left:
                    queue.append((node.left, pos * 2))
                if node.right:
                    queue.append((node.right, pos * 2 + 1))

            maxWidth = max(maxWidth, last_pos - first_pos + 1)

        return maxWidth


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
        ([1, 3, 2, 5, 3, None, 9],              4),
        ([1, 3, 2, 5, None, None, 9, 6, None, 7], 7),
        ([1, 3, 2, 5],                           2),
    ]

    for i, (input_list, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        output = sol.widthOfBinaryTree(root)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
