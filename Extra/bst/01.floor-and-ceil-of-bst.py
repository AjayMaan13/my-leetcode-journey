"""
Floor and Ceil of a BST
------------------------

Problem Statement:
Given a BST and a key, return [floor, ceil] where:
  - Floor: greatest node value <= key  (or -1 if none)
  - Ceil:  smallest node value >= key  (or -1 if none)

Example:
BST built from [8, 4, 12, 2, 6, 10, 14]:

         8
        / \\
       4   12
      / \\ / \\
     2  6 10  14

key=11 → [10, 12]   (10 is largest ≤ 11; 12 is smallest ≥ 11)
key=15 → [14, -1]   (no value ≥ 15 exists)
key=1  → [-1, 2]    (no value ≤ 1 exists)
key=8  → [8, 8]     (exact match)

─────────────────────────────────────────────────────────────────────────────
APPROACH 1 (mine) — two separate passes, one for floor, one for ceil
─────────────────────────────────────────────────────────────────────────────
Floor pass: walk the BST keeping a `lastVal` updated whenever we go right
  (i.e. whenever curr.data ≤ key, we have a candidate and explore larger values).
  When curr.data > key, prune right side and go left.

Ceil pass: mirror — keep `lastVal` updated whenever we go left
  (i.e. whenever curr.data ≥ key, we have a candidate and explore smaller values).
  When curr.data < key, go right.

─────────────────────────────────────────────────────────────────────────────
APPROACH 2 — single pass, both floor and ceil simultaneously
─────────────────────────────────────────────────────────────────────────────
BST ordering (left < node < right) lets us update both in one traversal:
  - curr.data == key → both are key, return immediately
  - curr.data < key  → candidate for floor, go right (look for something closer to key)
  - curr.data > key  → candidate for ceil, go left  (look for something closer to key)

O(h) time (h = height), O(1) space.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.data = val
        self.left = left
        self.right = right


def insert(node, val):
    if node is None:
        return TreeNode(val)
    if val < node.data:
        node.left = insert(node.left, val)
    else:
        node.right = insert(node.right, val)
    return node


def build_bst(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


class Solution:
    # Approach 1 — two separate passes
    def floorCeilOfBST_v1(self, root, key):
        def floorBST(root, key):
            curr, last = root, -1
            while curr:
                if curr.data <= key:
                    last = curr.data
                    curr = curr.right   # could be closer to key on the right
                else:
                    curr = curr.left    # too big, prune right
            return last

        def ceilBST(root, key):
            curr, last = root, -1
            while curr:
                if curr.data >= key:
                    last = curr.data
                    curr = curr.left    # could be closer to key on the left
                else:
                    curr = curr.right   # too small, prune left
            return last

        return [floorBST(root, key), ceilBST(root, key)]

    # Approach 2 — single pass, both at once
    def floorCeilOfBST(self, root, key):
        if not root:
            return [-1, -1]

        floor_val, ceil_val = -1, -1
        curr = root

        while curr:
            if curr.data == key:
                return [curr.data, curr.data]   # exact match
            elif curr.data < key:
                floor_val = curr.data           # candidate; look for closer on right
                curr = curr.right
            else:
                ceil_val = curr.data            # candidate; look for closer on left
                curr = curr.left

        return [floor_val, ceil_val]


if __name__ == "__main__":
    test_cases = [
        ([8, 4, 12, 2, 6, 10, 14], 11, [10, 12]),
        ([8, 4, 12, 2, 6, 10, 14], 15, [14, -1]),
        ([8, 4, 12, 2, 6, 10, 14],  1, [-1,  2]),
        ([8, 4, 12, 2, 6, 10, 14],  8, [ 8,  8]),
        ([5],                         5, [ 5,  5]),
        ([5],                        10, [ 5, -1]),
        ([5],                         1, [-1,  5]),
    ]

    sol = Solution()
    for i, (vals, key, expected) in enumerate(test_cases, 1):
        root = build_bst(vals)
        result = sol.floorCeilOfBST(root, key)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"Test {i}: {status} | key={key} | got {result} | expected {expected}")
