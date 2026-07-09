"""
Morris Inorder Traversal
-------------------------

Problem Statement:
Perform inorder traversal (Left → Root → Right) of a binary tree in O(n) time
and O(1) auxiliary space — no recursion stack, no explicit stack.

Example:
         1
        / \\
       2   3
      / \\
     4   5

Inorder: [4, 2, 5, 1, 3]

─────────────────────────────────────────────────────────────────────────────
KEY IDEA — Threaded Binary Tree
─────────────────────────────────────────────────────────────────────────────
Normal inorder recursion uses the call stack to "remember" where to come back
after finishing a left subtree. Morris Traversal avoids this by temporarily
wiring the INORDER PREDECESSOR of the current node to point BACK to the
current node. This creates a "thread" — a temporary right-pointer link.

The inorder predecessor of node X is the RIGHTMOST node of X's left subtree.
  - It's the last node visited before X in inorder order.
  - Its right pointer is normally None (it has no right child in the tree).
  - Morris exploits this free right pointer to create the thread.

─────────────────────────────────────────────────────────────────────────────
ALGORITHM  (for each position of `curr`)
─────────────────────────────────────────────────────────────────────────────
Case A — curr has NO left child:
    → Visit curr (record its value).
    → Move right:  curr = curr.right

Case B — curr HAS a left child:
    → Find the inorder predecessor (pred) = rightmost node in left subtree.

    Sub-case B1 — pred.right is None (thread NOT yet created):
        → Create thread:  pred.right = curr
        → Move left:      curr = curr.left
        (We'll come back to curr via the thread when the left subtree is done.)

    Sub-case B2 — pred.right is curr (thread ALREADY exists → we're back):
        → Remove thread:  pred.right = None   (restore tree)
        → VISIT curr      (left subtree fully processed, now record curr)
        → Move right:     curr = curr.right

Stop when curr is None.

─────────────────────────────────────────────────────────────────────────────
DRY RUN on the example tree
─────────────────────────────────────────────────────────────────────────────
         1
        / \\
       2   3
      / \\
     4   5

curr=1  → has left child 2
  pred of 1 = rightmost of {2,4,5} = 5   pred.right=None → B1
  thread: 5→1,  curr = 2

curr=2  → has left child 4
  pred of 2 = rightmost of {4} = 4       pred.right=None → B1
  thread: 4→2,  curr = 4

curr=4  → NO left child → Case A
  VISIT 4,  curr = curr.right = 2  (via thread)

curr=2  → has left child 4
  pred of 2 = 4,  pred.right = 2  → B2  (thread found!)
  remove thread,  VISIT 2,  curr = 5

curr=5  → NO left child → Case A
  VISIT 5,  curr = curr.right = 1  (via thread)

curr=1  → has left child 2
  pred of 1 = 5,  pred.right = 1  → B2  (thread found!)
  remove thread,  VISIT 1,  curr = 3

curr=3  → NO left child → Case A
  VISIT 3,  curr = None

Result: [4, 2, 5, 1, 3]  ✅

─────────────────────────────────────────────────────────────────────────────
COMPLEXITY
─────────────────────────────────────────────────────────────────────────────
Time:  O(n)  — each node is visited at most twice (once to set thread, once
               to unset it and record value)
Space: O(1)  — no stack or recursion; only `curr` and `pred` pointers
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def morrisInorder(root):
    result = []
    curr = root

    while curr:
        if not curr.left:
            # Case A: no left child — visit and go right
            result.append(curr.val)
            curr = curr.right
        else:
            # Find inorder predecessor (rightmost node of left subtree)
            pred = curr.left
            while pred.right and pred.right is not curr:
                pred = pred.right

            if pred.right is None:
                # B1: thread not set — create it and dive left
                pred.right = curr
                curr = curr.left
            else:
                # B2: thread exists — left subtree done, visit curr
                pred.right = None       # remove thread (restore tree)
                result.append(curr.val)
                curr = curr.right

    return result


if __name__ == "__main__":
    #       1
    #      / \
    #     2   3
    #    / \
    #   4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)

    print("Morris Inorder:", morrisInorder(root))
    # Expected: [4, 2, 5, 1, 3]
