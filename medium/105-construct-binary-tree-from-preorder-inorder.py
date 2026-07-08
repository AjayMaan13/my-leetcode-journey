from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ❌ Attempt 1 — correct logic, but missing `return node` at the end of findLR.
# Because there's no return, findLR always returns None, so the result is None.
class Solution(object):
    def buildTree_v1(self, preorder, inorder):
        def findLR(preorder, inorder):
            if not preorder:
                return None

            root = preorder[0]
            i = inorder.index(root)          # O(n) scan per call

            leftIn  = inorder[:i]
            rightIn = inorder[i + 1:]

            n_left  = len(leftIn)
            leftPre  = preorder[1:1 + n_left]
            rightPre = preorder[1 + n_left:]

            node = TreeNode(root)
            node.left  = findLR(leftPre, leftIn)
            node.right = findLR(rightPre, rightIn)

            return node                       # ← this line was missing in attempt

        return findLR(preorder, inorder)


# ✅ Optimised — O(n) time, no slicing
#
# Two expensive things in the naive version:
#   1. inorder.index(root)  → O(n) linear scan on every recursive call
#   2. slicing leftPre / rightPre / leftIn / rightIn → O(k) copies each call
#
# Fixes:
#   CHANGE 1: Build idx_map {value: index} from inorder once → O(1) lookup.
#   CHANGE 2: Use self.pre_idx pointer that advances through preorder without
#             ever copying it. Pointer must be consumed left-subtree first to
#             match preorder's root→left→right ordering.
#   CHANGE 3: Pass inorder boundaries (left, right) instead of sliced lists.
class Solution(object):
    def buildTree(self, preorder, inorder):
        """
        :type preorder: List[int]
        :type inorder: List[int]
        :rtype: Optional[TreeNode]
        """
        idx_map = {val: i for i, val in enumerate(inorder)}
        self.pre_idx = 0

        def findLR(left, right):
            if left > right:
                return None

            root_val = preorder[self.pre_idx]
            self.pre_idx += 1

            node = TreeNode(root_val)

            i = idx_map[root_val]

            # Left MUST come before right — pre_idx advances in preorder order
            node.left  = findLR(left,  i - 1)
            node.right = findLR(i + 1, right)

            return node

        return findLR(0, len(inorder) - 1)


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
        ([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),
        ([-1], [-1], [-1]),
    ]

    for i, (preorder, inorder, expected_list) in enumerate(test_cases, 1):
        root = sol.buildTree(preorder, inorder)
        output = levelOrder(root)
        expected = levelOrder(buildFromList(expected_list))
        status = "✅ Passed" if output == expected else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Preorder: {preorder}")
        print(f"  Inorder:  {inorder}")
        print(f"  Expected: {expected}")
        print(f"  Got:      {output}\n")
