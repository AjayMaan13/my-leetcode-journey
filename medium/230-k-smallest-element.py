"""
230. Kth Smallest Element in a BST (LeetCode - Medium)

Problem Statement:
------------------
Given the root of a binary search tree, and an integer k, 
return the kth smallest value (1-indexed) of all the values of the nodes in the tree.

Example 1:
----------
Input: root = [3,1,4,null,2], k = 1
Output: 1

Example 2:
----------
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3

Constraints:
------------
- The number of nodes in the tree is n.
- 1 <= k <= n <= 10^4
- 0 <= Node.val <= 10^4

Follow-up:
----------
If the BST is modified often (i.e., insert/delete operations happen frequently) 
and you need to find the kth smallest frequently, how would you optimize?
"""

# -------------------------------
# Definition for a binary tree node.
# -------------------------------
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# -------------------------------
#  My Solution 
# -------------------------------
class Solution(object):
    def kthSmallest(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """
        
        def inorderList(node):
            if not node:
                return []
            
            return inorderList(node.left) + [node.val] + inorderList(node.right)

        inorderList_result = inorderList(root)

        return inorderList_result[k - 1]

# -------------------------------
# Optimized Solution (Inorder Early Stop)
# -------------------------------
class Solution(object):
    def kthSmallest(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """

        self.k = k
        self.result = None

        def inorder(node):
            if not node or self.result is not None:
                return

            inorder(node.left)   # Visit left subtree

            # Process current node
            self.k -= 1
            if self.k == 0:
                self.result = node.val
                return

            inorder(node.right)  # Visit right subtree

        inorder(root)
        return self.result

class Solution(object):
    def kthSmallest(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """
        stack = []
        curr = root

        while stack or curr:
            # phase 1: go as far left as possible, pushing every
            # node along the way so we can come back to it later
            while curr:
                stack.append(curr)
                curr = curr.left

            # phase 2: no more left to explore — pop the most
            # recently pushed node, this is the next node in
            # ascending order (the "visit")
            curr = stack.pop()
            k -= 1
            if k == 0:
                return curr.val

            # phase 3: left subtree (and this node) are done,
            # now explore the right subtree
            curr = curr.right

        return -1  # k was larger than the number of nodes in the tree
class Solution(object):
    def kthSmallest(self, root, k):
        """
        :type root: Optional[TreeNode]
        :type k: int
        :rtype: int
        """
        count = 0       # tracks how many nodes we've visited in ascending order
        curr = root

        while curr:
            if curr.left is None:
                # no left subtree to explore — this node is next in
                # ascending order, so it's a real visit
                count += 1
                if count == k:
                    return curr.val
                curr = curr.right          # nothing more on the left, move right

            else:
                # find the inorder predecessor: rightmost node of
                # curr's left subtree — this is where we'll thread
                # a temporary pointer back to curr
                pred = curr.left
                while pred.right and pred.right != curr:
                    pred = pred.right

                if pred.right is None:
                    # first time arriving at curr — thread it so we
                    # can find our way back after exploring the left
                    # subtree, then dive left
                    pred.right = curr
                    curr = curr.left

                else:
                    # second time arriving at curr — the thread led us
                    # back here, meaning the left subtree is fully done.
                    # remove the thread (restore original tree shape),
                    # then this is a real visit
                    pred.right = None
                    count += 1
                    if count == k:
                        return curr.val
                    curr = curr.right       # left subtree done, move right

        return -1  # k was larger than the number of nodes in the tree

# -------------------------------
# Helper Functions for Testing
# -------------------------------
def build_tree(values):
    """
    Build binary tree from level-order list (like LeetCode input format).
    Example: [3,1,4,None,2] -> Tree structure
    """
    if not values:
        return None

    from collections import deque
    iter_vals = iter(values)
    root = TreeNode(next(iter_vals))
    queue = deque([root])

    for val in iter_vals:
        node = queue.popleft()
        if val is not None:
            node.left = TreeNode(val)
            queue.append(node.left)
        try:
            val = next(iter_vals)
            if val is not None:
                node.right = TreeNode(val)
                queue.append(node.right)
        except StopIteration:
            break

    return root


def test():
    sol = Solution()

    # Test Case 1
    root = build_tree([3,1,4,None,2])
    print("Expected: 1, Got:", sol.kthSmallest(root, 1))

    # Test Case 2
    root = build_tree([5,3,6,2,4,None,None,1])
    print("Expected: 3, Got:", sol.kthSmallest(root, 3))


if __name__ == "__main__":
    test()
