"""
Iterative Postorder Traversal of Binary Tree Using 2 Stacks
------------------------------------------------------------

Problem Statement:
Given the root of a Binary Tree, perform a postorder traversal iteratively
using two stacks and return the traversal sequence.

Example 1:
Input:  4 2 5 3 -1 7 6 -1 9 -1 -1 8 -1 1
Output: [1, 9, 3, 2, 7, 8, 6, 5, 4]

Example 2:
Input:  1 2 3 4 5 6 7 -1 -1 8 -1 -1 -1 9 10
Output: [4, 8, 5, 2, 6, 9, 10, 7, 3, 1]

Approach:
st1 drives a root→right→left traversal (push left then right so right pops first).
Every popped node goes onto st2. When st1 is empty, st2 holds nodes in
root→right→left order — popping st2 reverses that to left→right→root = postorder.

Related: easy/145-binary-tree-postorder-traversal.py
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def postOrder(root):
    if root is None:
        return []

    st1, st2 = [root], []

    while st1:
        node = st1.pop()
        st2.append(node)
        if node.left:
            st1.append(node.left)
        if node.right:
            st1.append(node.right)

    result = []
    while st2:
        result.append(st2.pop().val)

    return result


if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    print("Postorder traversal:", postOrder(root))
