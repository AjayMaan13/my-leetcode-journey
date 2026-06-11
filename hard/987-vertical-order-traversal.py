from collections import deque, defaultdict

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ❌ Attempt 1 — did not work
# getLeftRightEnds only walks the leftmost/rightmost spine, so it misses
# nodes that are further out via a mix of left/right turns.
# Also DFS here doesn't track row, so same-column nodes at different depths
# are not sorted correctly when there are ties.
class Solution(object):
    def verticalTraversal(self, root):
        self.res = []

        def getLeftRightEnds(root):
            temp = root
            left = 0
            right = 0
            while temp.left:
                temp = temp.left
                left += 1
            temp = root
            while temp.right:
                temp = temp.right
                right += 1
            return 0, left + 1, left + right + 1

        def levelDFS(node, x):
            self.res[x - 1].append(node.val)
            if node.left: levelDFS(node.left, x - 1)
            if node.right: levelDFS(node.right, x + 1)

        left, mid, right = getLeftRightEnds(root)
        for _ in range(right):
            self.res.append([])
        levelDFS(root, mid)
        return self.res


# ❌ Attempt 2 — did not work
# BFS tracks column but NOT row, so when two nodes share a column at different
# depths the values end up in insertion (BFS level) order rather than being
# sorted by (row, value) as the problem requires.
class Solution(object):
    def verticalTraversal(self, root):
        if not root:
            return []

        q = deque([(root, 0)])
        min_col = max_col = 0
        cols = defaultdict(list)

        while q:
            node, col = q.popleft()
            cols[col].append(node.val)
            min_col = min(min_col, col)
            max_col = max(max_col, col)
            if node.left:
                q.append((node.left, col - 1))
            if node.right:
                q.append((node.right, col + 1))

        return [cols[c] for c in range(min_col, max_col + 1)]


# ✅ Attempt 3 — BFS, collect (col, row, val), sort, group
# Key insight: store row alongside col so ties (same col AND same row)
# can be broken by value. Sorting the flat list by (col, row, val) in one
# step handles all ordering rules at once.
class Solution(object):
    def verticalTraversal(self, root):
        if not root:
            return []

        nodes = []
        q = deque([(root, 0, 0)])  # (node, col, row)

        while q:
            node, x, y = q.popleft()
            nodes.append((x, y, node.val))
            if node.left:
                q.append((node.left, x - 1, y + 1))
            if node.right:
                q.append((node.right, x + 1, y + 1))

        nodes.sort()  # sorts by col, then row, then val

        res = []
        prev_x = float('-inf')
        col = []
        for x, y, val in nodes:
            if x != prev_x:
                if col:
                    res.append(col)
                col = []
                prev_x = x
            col.append(val)
        if col:
            res.append(col)
        return res


# ✅ Attempt 4 — DFS variant, same idea as attempt 3
# DFS instead of BFS — both work because sorting handles ordering,
# not traversal order. Slightly cleaner grouping with res[-1].
class Solution(object):
    def verticalTraversal(self, root):
        nodes = []

        def dfs(node, row, col):
            if not node:
                return
            nodes.append((col, row, node.val))
            dfs(node.left, row + 1, col - 1)
            dfs(node.right, row + 1, col + 1)

        dfs(root, 0, 0)
        nodes.sort()

        res = []
        prev_col = float('-inf')
        for col, row, val in nodes:
            if col != prev_col:
                res.append([])
                prev_col = col
            res[-1].append(val)
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
        ([3, 9, 20, None, None, 15, 7],  [[9], [3, 15], [20], [7]]),
        ([1, 2, 3, 4, 5, 6, 7],          [[4], [2], [1, 5, 6], [3], [7]]),
        ([1, 2, 3, 4, 6, 5, 7],          [[4], [2], [1, 5, 6], [3], [7]]),
    ]

    for i, (input_list, expected) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        output = sol.verticalTraversal(root)
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input:    {input_list}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
