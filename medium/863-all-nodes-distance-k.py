from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# BFS from target treating the tree as an undirected graph.
# Problem: trees only have parent→child edges, so we can't walk upward.
# Solution: first DFS to build a parent map, then BFS in all 3 directions
#           (left child, right child, parent) from the target.
class Solution(object):
    def distanceK(self, root, target, k):
        """
        :type root: TreeNode
        :type target: TreeNode
        :type k: int
        :rtype: List[int]
        """
        # Step 1: record each node's parent
        parent = {}

        def buildParents(node, par):
            if not node:
                return
            parent[node] = par
            buildParents(node.left, node)
            buildParents(node.right, node)

        buildParents(root, None)

        # Step 2: BFS from target, distance k
        queue = deque([(target, 0)])
        visited = {target}
        res = []

        while queue:
            node, dist = queue.popleft()
            if dist == k:
                res.append(node.val)
                continue  # no need to go deeper

            for neighbour in (node.left, node.right, parent[node]):
                if neighbour and neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, dist + 1))

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


def findNode(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    return findNode(root.left, val) or findNode(root.right, val)


# ✅ Tester
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 2, sorted([7, 4, 1])),
        ([1], 1, 3, []),
    ]

    for i, (input_list, target_val, k, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        target = findNode(root, target_val)
        output = sorted(sol.distanceK(root, target, k))
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}, target={target_val}, k={k}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
