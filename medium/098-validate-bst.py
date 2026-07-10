"""
LeetCode Problem: 98. Validate Binary Search Tree
Link: https://leetcode.com/problems/validate-binary-search-tree/

Description:
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as:
1. The left subtree of a node contains only nodes with keys strictly less than the node's key.
2. The right subtree of a node contains only nodes with keys strictly greater than the node's key.
3. Both the left and right subtrees must also be binary search trees.

Example 1:
Input: root = [2,1,3]
Output: true

Example 2:
Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.

Constraints:
- The number of nodes in the tree is in the range [1, 10^4].
- -2^31 <= Node.val <= 2^31 - 1
"""

# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# My solution, O(n)-time and space
class Solution(object):
    def isValidBST(self, root):
        
        #:type root: TreeNode
        #:rtype: bool
        
        if not root:
            return
        
        isBST = True
        inorderList = []

        def inorder(root):
            
            if not root:
                return
            inorder(root.left)
            inorderList.append(root.val)
            inorder(root.right)

        inorder(root)
        length = len(inorderList) 
        left = 0
        right = 1
        while right < length:
            if inorderList[left] >= inorderList[right]:
                isBST = False
            left += 1
            right += 1
        
        return isBST

# Optimized Solution with Log^2(n) time complexity
class Solution(object):
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """

        # Keep track of the previously visited value during in-order traversal
        self.prev = None

        def inorder(node):
            if not node:
                return True

            # ✅ 1. Go to the left subtree
            if not inorder(node.left):
                return False

            # ✅ 2. Check current node value
            # If the current value is NOT greater than the previous value → not a BST
            if self.prev is not None and node.val <= self.prev:
                return False

            # ✅ 3. Update previous value to current node value
            self.prev = node.val

            # ✅ 4. Go to the right subtree
            return inorder(node.right)

        return inorder(root)


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 3 — bounds-check recursive (range propagation)
#
# Pass down valid [low, high) range for each node.
# Left subtree: upper bound tightens to parent value.
# Right subtree: lower bound tightens to parent value.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def isValidBST(self, root):
        def helper(node, low, high):
            if not node:
                return True
            if not (low < node.val < high):
                return False
            return helper(node.left, low, node.val) and helper(node.right, node.val, high)
        return helper(root, float('-inf'), float('inf'))


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 4 — iterative inorder with explicit stack
#
# Same logic as Solution 2 but avoids Python recursion stack.
# Walk left as far as possible, then pop and check against prev.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def isValidBST(self, root):
        stack, curr, prev = [], root, None
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            if prev is not None and curr.val <= prev:
                return False
            prev = curr.val
            curr = curr.right
        return True


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Solution 5 — Morris inorder (O(1) space, no stack, no recursion)
#
# Thread each node's inorder predecessor's right pointer back to the node.
# When we arrive via the thread we unthread, visit, and move right.
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def isValidBST(self, root):
        prev, curr = None, root
        while curr:
            if curr.left is None:
                if prev is not None and curr.val <= prev:
                    return False
                prev = curr.val
                curr = curr.right
            else:
                # find inorder predecessor
                pred = curr.left
                while pred.right and pred.right != curr:
                    pred = pred.right
                if pred.right is None:
                    pred.right = curr       # thread: will return here later
                    curr = curr.left
                else:
                    pred.right = None       # unthread
                    if prev is not None and curr.val <= prev:
                        return False
                    prev = curr.val
                    curr = curr.right
        return True


# ---------------------------
# 🔹 Example to understand in-place check
# ---------------------------

# Example Tree (Valid BST):
#        2
#       / \
#      1   3
#
# In-order traversal steps:
#   1️⃣ Go to left → visit 1 → prev = 1
#   2️⃣ Visit root 2 → compare 2 > 1 ✅ → prev = 2
#   3️⃣ Go to right → visit 3 → compare 3 > 2 ✅ → prev = 3
# Output = True ✅


# Example Tree (Invalid BST):
#        5
#       / \
#      1   4
#         / \
#        3   6
#
# In-order traversal steps:
#   1️⃣ Go left → visit 1 → prev = 1
#   2️⃣ Visit 5 → compare 5 > 1 ✅ → prev = 5
#   3️⃣ Go right → visit 3 → compare 3 > 5 ❌ (Invalid)
# Immediately return False → No need to check further.

# ---------------------------
# The check is "in-place" because:
#  - We update `self.prev` while traversing (no extra list).
#  - We stop early as soon as we find a violation.


    
# ----------------------
# Testing Code
# ----------------------

def build_tree_from_list(values):
    """Helper to build tree from level-order list."""
    if not values:
        return None

    from collections import deque
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


if __name__ == "__main__":
    # Test Case 1
    root1 = build_tree_from_list([2, 1, 3])
    print("Expected: True")
    print("Output:", Solution().isValidBST(root1))

    # Test Case 2
    root2 = build_tree_from_list([5, 1, 4, None, None, 3, 6])
    print("Expected: False")
    print("Output:", Solution().isValidBST(root2))

    root3 = build_tree_from_list([2,2,2])
    print("Expected: False")
    print("Output:", Solution().isValidBST(root3))
