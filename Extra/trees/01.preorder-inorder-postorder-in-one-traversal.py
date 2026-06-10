"""
Preorder Inorder Postorder Traversals in One Traversal
-------------------------------------------------------

Problem Statement:
Given the root of a Binary Tree, return the preorder, inorder and postorder
traversal sequences by making just one traversal.

Example 1:
Input:  4 2 5 3 -1 7 6 -1 9 -1 -1 8 -1 1
Output:
  Preorder:  [4, 2, 3, 9, 1, 5, 7, 6, 8]
  Inorder:   [3, 1, 9, 2, 4, 7, 5, 8, 6]
  Postorder: [1, 9, 3, 2, 7, 8, 6, 5, 4]

Example 2:
Input:  1 2 3 4 5 6 7 -1 -1 8 -1 -1 -1 9 10
Output:
  Preorder:  [1, 2, 4, 5, 8, 3, 6, 7, 9, 10]
  Inorder:   [4, 2, 8, 5, 1, 6, 3, 9, 7, 10]
  Postorder: [4, 8, 5, 2, 6, 9, 10, 7, 3, 1]

Approach:
Use a stack that stores (node, state) pairs. Each node passes through 3 states:
  state 1 → preorder:   record val, push left child, advance to state 2
  state 2 → inorder:    record val, push right child, advance to state 3
  state 3 → postorder:  record val, pop (done)
"""


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


class Solution:
    def preInPostTraversal(self, root):
        pre, ino, post = [], [], []

        if root is None:
            return [pre, ino, post]

        # Each stack entry is (node, state): 1=pre, 2=in, 3=post
        st = [(root, 1)]

        while st:
            node, state = st.pop()

            if state == 1:
                pre.append(node.data)
                st.append((node, 2))
                if node.left:
                    st.append((node.left, 1))

            elif state == 2:
                ino.append(node.data)
                st.append((node, 3))
                if node.right:
                    st.append((node.right, 1))

            else:
                post.append(node.data)

        return [pre, ino, post]


if __name__ == "__main__":
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)

    sol = Solution()
    pre, ino, post = sol.preInPostTraversal(root)

    print("Preorder:  ", pre)
    print("Inorder:   ", ino)
    print("Postorder: ", post)
