from collections import deque

# ✅ TreeNode definition
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Version 1 — recursive with standalone findMin helper
#
# Three deletion cases:
#   1. No left child  → replace node with its right subtree
#   2. No right child → replace node with its left subtree
#   3. Two children   → find inorder successor (leftmost of right subtree),
#                       copy its value up, then delete it from the right subtree
# ─────────────────────────────────────────────────────────────────────────────
def findMin(node):
    while node.left:
        node = node.left
    return node


class Solution(object):
    def deleteNode_v1(self, root, key):
        if root is None:
            return None
        if key < root.val:
            root.left = self.deleteNode_v1(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode_v1(root.right, key)
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left
            successor = findMin(root.right)
            root.val = successor.val
            root.right = self.deleteNode_v1(root.right, successor.val)
        return root


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Version 2 — iterative with explicit parent (pred) tracking
#
# Walk to the target node keeping track of its parent (pred) and which side
# (pred.left vs pred.right) points to it. Then handle all four cases:
#   - Two children: copy successor value, recursively delete successor
#   - Left child only / Right child only / Leaf: rewire parent pointer
#
# Explicit pred tracking avoids recursion stack but adds code for each case.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def deleteNode_v2(self, root, key):
        def findSuccessor(node):
            curr = node.right
            while curr.left:
                curr = curr.left
            return curr

        pred, curr = None, root

        while curr:
            if curr.val == key:
                if curr.left and curr.right:
                    successor = findSuccessor(curr)
                    curr.val = successor.val
                    curr.right = self.deleteNode_v2(curr.right, successor.val)
                    return root
                elif curr.left:
                    child = curr.left
                elif curr.right:
                    child = curr.right
                else:
                    child = None

                if pred is None:
                    return child
                if pred.left == curr:
                    pred.left = child
                else:
                    pred.right = child
                return root
            else:
                pred = curr
                curr = curr.left if curr.val > key else curr.right

        return root


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Version 3 — concise recursive (cleanest)
#
# Same logic as v1 but self-contained: findMin inlined as a local while-loop.
# Most interview-friendly version.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def deleteNode(self, root, key):
        """
        :type root: Optional[TreeNode]
        :type key: int
        :rtype: Optional[TreeNode]
        """
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            # two children: find inorder successor (min of right subtree)
            curr = root.right
            while curr.left:
                curr = curr.left
            root.val = curr.val
            root.right = self.deleteNode(root.right, curr.val)
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


def inorder(root):
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)


# ✅ Tester
if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([5, 3, 6, 2, 4, None, 7], 3, [2, 4, 5, 6, 7]),   # delete internal node
        ([5, 3, 6, 2, 4, None, 7], 0, [2, 3, 4, 5, 6, 7]), # key not in tree
        ([],                        0, []),                  # empty tree
        ([5, 3, 6, 2, 4, None, 7], 5, [2, 3, 4, 6, 7]),    # delete root
    ]

    for i, (input_list, key, expected_inorder) in enumerate(test_cases, 1):
        root = buildTree(input_list)
        result = sol.deleteNode(root, key)
        output = inorder(result)
        status = "✅ Passed" if output == expected_inorder else "❌ Failed"
        print(f"Test {i}: {status}")
        print(f"  Input: {input_list}, key={key}")
        print(f"  Expected (inorder): {expected_inorder}")
        print(f"  Got:                {output}\n")
