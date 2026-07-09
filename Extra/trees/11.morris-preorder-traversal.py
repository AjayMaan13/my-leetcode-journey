"""
Morris Preorder Traversal
--------------------------

Problem Statement:
Perform preorder traversal (Root → Left → Right) of a binary tree in O(n) time
and O(1) auxiliary space — no recursion stack, no explicit stack.

Example:
         1
        / \\
       2   3
      / \\
     4   5

Preorder: [1, 2, 4, 5, 3]

─────────────────────────────────────────────────────────────────────────────
DIFFERENCE FROM MORRIS INORDER
─────────────────────────────────────────────────────────────────────────────
In inorder we VISIT the node when we REMOVE the thread (sub-case B2) —
because that's when the left subtree is fully done.

In preorder we VISIT the node when we CREATE the thread (sub-case B1) —
because preorder visits the root BEFORE the left subtree.

One-line diff:
  Inorder  → visit in B2 (thread removal)
  Preorder → visit in B1 (thread creation) and in Case A (no left child)

Everything else (finding the predecessor, setting/unsetting threads) is
identical.

─────────────────────────────────────────────────────────────────────────────
ALGORITHM
─────────────────────────────────────────────────────────────────────────────
Case A — curr has NO left child:
    → VISIT curr.
    → Move right:  curr = curr.right

Case B — curr HAS a left child:
    → Find pred = rightmost node of left subtree (inorder predecessor).

    Sub-case B1 — pred.right is None (first time visiting curr):
        → VISIT curr      ← preorder visits root BEFORE diving left
        → Create thread:  pred.right = curr
        → Move left:      curr = curr.left

    Sub-case B2 — pred.right is curr (returning via thread):
        → Remove thread:  pred.right = None
        → Do NOT visit    ← already visited in B1
        → Move right:     curr = curr.right

─────────────────────────────────────────────────────────────────────────────
DRY RUN on the example tree
─────────────────────────────────────────────────────────────────────────────
         1
        / \\
       2   3
      / \\
     4   5

curr=1  → has left 2
  pred = rightmost of {2,4,5} = 5   pred.right=None → B1
  VISIT 1,  thread: 5→1,  curr = 2

curr=2  → has left 4
  pred = rightmost of {4} = 4        pred.right=None → B1
  VISIT 2,  thread: 4→2,  curr = 4

curr=4  → NO left → Case A
  VISIT 4,  curr = 2  (via thread)

curr=2  → has left 4
  pred = 4,  pred.right = 2 → B2  (thread found!)
  remove thread,  curr = 5

curr=5  → NO left → Case A
  VISIT 5,  curr = 1  (via thread)

curr=1  → has left 2
  pred = 5,  pred.right = 1 → B2  (thread found!)
  remove thread,  curr = 3

curr=3  → NO left → Case A
  VISIT 3,  curr = None

Result: [1, 2, 4, 5, 3]  ✅

─────────────────────────────────────────────────────────────────────────────
COMPLEXITY
─────────────────────────────────────────────────────────────────────────────
Time:  O(n)  — each node processed at most twice
Space: O(1)  — only two pointers, no stack
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def morrisPreorder(root):
    result = []
    curr = root

    while curr:
        if not curr.left:
            # Case A: no left child — visit and go right
            result.append(curr.val)
            curr = curr.right
        else:
            # Find inorder predecessor
            pred = curr.left
            while pred.right and pred.right is not curr:
                pred = pred.right

            if pred.right is None:
                # B1: first visit — VISIT now (preorder), then thread and go left
                result.append(curr.val)
                pred.right = curr
                curr = curr.left
            else:
                # B2: returning via thread — already visited, just clean up
                pred.right = None       # remove thread (restore tree)
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

    print("Morris Preorder:", morrisPreorder(root))
    # Expected: [1, 2, 4, 5, 3]
