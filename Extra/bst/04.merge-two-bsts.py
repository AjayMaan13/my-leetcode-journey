"""
Merge Two BSTs
--------------
TakeUForward — Extra BST

Problem Statement:
Given two BSTs, return all elements of both trees merged in sorted order.

Example 1:
  BST1: [5, 3, 6, 2, 4]      BST2: [2, 1, 3, null, null, null, 7]
  Output: [1, 2, 2, 3, 3, 4, 5, 6, 7]

Example 2:
  BST1: [12, 9, null, 6, 11]  BST2: [8, 5, 10, 2]
  Output: [2, 5, 6, 8, 9, 10, 11, 12]

─────────────────────────────────────────────────────────────────────────────
Approaches:
  Brute:   traverse both trees (any order) → merge into one list → sort
  Optimal: inorder both trees → two SORTED lists → merge with two pointers
  Best:    two BSTIterators (lazy inorder stacks) → merge on-the-fly → O(h) space
─────────────────────────────────────────────────────────────────────────────
"""


class Node:
    def __init__(self, val):
        self.data = val
        self.left = None
        self.right = None


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 1 — brute force: traverse both + sort
#
# Collect every node value from both trees (order doesn't matter during
# traversal), then sort the combined list.
# Time: O((m+n) log(m+n))   Space: O(m+n) for the list
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def _collect(self, root, out):
        if not root:
            return
        self._collect(root.left, out)
        out.append(root.data)
        self._collect(root.right, out)

    def mergeBSTs_v1(self, root1, root2):
        elements = []
        self._collect(root1, elements)
        self._collect(root2, elements)
        elements.sort()
        return elements


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 2 — inorder both trees → merge two sorted lists (optimal)
#
# Inorder traversal of a BST yields a sorted list.
# Merging two sorted lists with two pointers is O(m+n) — no sort needed.
# Time: O(m+n)   Space: O(m+n)
#
# Merge step:
#   i points into list1, j points into list2.
#   Always pick the smaller of list1[i] / list2[j], advance that pointer.
#   Drain whichever list still has elements at the end.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def _inorder(self, root, out):
        if not root:
            return
        self._inorder(root.left, out)
        out.append(root.data)
        self._inorder(root.right, out)

    def _merge(self, a, b):
        merged = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                merged.append(a[i]); i += 1
            else:
                merged.append(b[j]); j += 1
        # drain remaining
        merged.extend(a[i:])
        merged.extend(b[j:])
        return merged

    def mergeBSTs_v2(self, root1, root2):
        list1, list2 = [], []
        self._inorder(root1, list1)
        self._inorder(root2, list2)
        return self._merge(list1, list2)


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 3 — two BSTIterators, merge on-the-fly  (best space)
#
# Same two-pointer merge but we never materialise the full inorder lists.
# Each iterator holds only the current left-spine on a stack → O(h1 + h2) space.
# Time: O(m+n)   Space: O(h1 + h2)  where h = height of each tree
#
# This is the BSTIterator pattern (Extra/bst/03) applied to two trees at once.
# ─────────────────────────────────────────────────────────────────────────────
class _BSTIter:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def has_next(self):
        return bool(self.stack)

    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)
        return node.data


class Solution:
    def mergeBSTs(self, root1, root2):
        it1 = _BSTIter(root1)
        it2 = _BSTIter(root2)
        result = []

        # peek values from each iterator, always consume the smaller one
        v1 = it1.next() if it1.has_next() else None
        v2 = it2.next() if it2.has_next() else None

        while v1 is not None and v2 is not None:
            if v1 <= v2:
                result.append(v1)
                v1 = it1.next() if it1.has_next() else None
            else:
                result.append(v2)
                v2 = it2.next() if it2.has_next() else None

        # drain whichever iterator still has values
        while v1 is not None:
            result.append(v1)
            v1 = it1.next() if it1.has_next() else None
        while v2 is not None:
            result.append(v2)
            v2 = it2.next() if it2.has_next() else None

        return result


# ─────────────────────────────────────────────────────────────────────────────
# Helpers for testing
# ─────────────────────────────────────────────────────────────────────────────
def insert(root, val):
    if not root:
        return Node(val)
    if val < root.data:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root


def build_bst(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


if __name__ == "__main__":
    sol = Solution()

    test_cases = [
        ([2, 1, 4],    [3, 0, 5],        [0, 1, 2, 3, 4, 5]),
        ([5, 3, 6, 2, 4], [2, 1, 3, 7],  [1, 2, 2, 3, 3, 4, 5, 6, 7]),
        ([12, 9, 6, 11],   [8, 5, 10, 2], [2, 5, 6, 8, 9, 10, 11, 12]),
        ([1],              [2],            [1, 2]),
    ]

    for fn_name, fn in [("v1 brute",    sol.mergeBSTs_v1),
                        ("v2 inorder",  sol.mergeBSTs_v2),
                        ("v3 iterator", sol.mergeBSTs)]:
        print(f"\n── {fn_name} ──")
        for vals1, vals2, expected in test_cases:
            r1 = build_bst(vals1)
            r2 = build_bst(vals2)
            result = fn(r1, r2)
            status = "✅" if result == expected else "❌"
            print(f"  {status} BST1={vals1} + BST2={vals2}")
            print(f"       got={result}")
            print(f"       exp={expected}")
