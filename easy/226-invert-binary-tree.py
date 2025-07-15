from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# My solution here
class Solution(object):
    def invertTree(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: Optional[TreeNode]
        """
        print(f"Entered invertTree func")
        if not root or (not root.left and not root.right):
            return root
        else:
            root.left,root.right = root.right,root.left

            if root.left: self.invertTree(root.left)
            if root.right: self.invertTree(root.right)
        
        return root

# More Cleaner code:
class Solution(object):
    def invertTree(self, root):
        if not root:
            return None
        
        # Swap the left and right children
        root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root

# Iterative BFS
from collections import deque

class Solution(object):
    def invertTree(self, root):
        if not root:
            return None
        
        queue = deque([root])
        while queue:
            node = queue.popleft()
            node.left, node.right = node.right, node.left
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
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

# ✅ Convert tree to list (level order)
def treeToList(root):
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.val if node else None)

        if node:
            queue.append(node.left)
            queue.append(node.right)

    # Trim trailing None values
    while result and result[-1] is None:
        result.pop()

    return result

# ✅ Tester
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([4,2,7,1,3,6,9], [4,7,2,9,6,3,1]),
        ([2,1,3], [2,3,1]),
        ([], []),
        ([1], [1]),
        ([1,2], [1,None,2])
    ]

    for i, (input_list, expected_output) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        inverted = sol.invertTree(root)
        output_list = treeToList(inverted)
        print(f"Test {i}: {'✅ Passed' if output_list == expected_output else '❌ Failed'}")
        print(f"Input:    {input_list}")
        print(f"Expected: {expected_output}")
        print(f"Got:      {output_list}\n")
