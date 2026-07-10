"""
Predecessor and Successor in BST
----------------------------------

Problem Statement:
Given a BST and a key, return (predecessor, successor) where:
  - Predecessor: largest node value strictly LESS THAN key    (or None if none)
  - Successor:   smallest node value strictly GREATER THAN key (or None if none)

Note: unlike floor/ceil, exact matches at the key itself are NOT valid answers.

Example:
BST built from [8, 4, 12, 2, 6, 10, 14]:

         8
        / \\
       4   12
      / \\ / \\
     2  6 10  14

key=8  → pred=6,    succ=10   (8 itself is excluded)
key=11 → pred=10,   succ=12
key=15 → pred=14,   succ=None
key=1  → pred=None, succ=2

─────────────────────────────────────────────────────────────────────────────
Comparison with Floor/Ceil (from 01.floor-and-ceil-of-bst.py):
  floor/ceil  use  <=  /  >=  → key itself IS a valid answer
  pred/succ   use  <   /  >   → key itself is NOT a valid answer

The only code difference is swapping <= for < and >= for > in the walk condition.
─────────────────────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 1 — Brute force: full inorder list + binary search
#
# Build the sorted inorder list (O(n)), then binary search for the key.
# Predecessor is the element just before the key's position; successor just after.
# O(n) time, O(n) space.
# ─────────────────────────────────────────────────────────────────────────────
def predecessorSuccessor_v1(root, key):
    inorder = []

    def traverse(node):
        if not node:
            return
        traverse(node.left)
        inorder.append(node.data)
        traverse(node.right)

    traverse(root)

    pred, succ = None, None
    lo, hi = 0, len(inorder) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if inorder[mid] < key:
            pred = inorder[mid]
            lo = mid + 1
        elif inorder[mid] > key:
            succ = inorder[mid]
            hi = mid - 1
        else:
            # exact match: neighbors are predecessor and successor
            if mid - 1 >= 0:
                pred = inorder[mid - 1]
            if mid + 1 < len(inorder):
                succ = inorder[mid + 1]
            break

    return pred, succ


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 2 — iterative inorder, early exit
#
# Walk inorder with an explicit stack. Track `prev` (last visited node).
# Stop as soon as we've seen the successor (first node > key).
# O(h + k) time where k = nodes visited before finding successor, O(h) space.
#
# Could replace the stack with Morris traversal to get O(1) space.
# ─────────────────────────────────────────────────────────────────────────────
def predecessorSuccessor_v2(root, key):
    pred, succ = None, None
    stack = []
    curr = root
    prev = None

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()

        # prev < key <= curr → prev is the predecessor
        if prev is not None and prev.data < key <= curr.data:
            pred = prev
        # first node strictly greater than key → successor
        if curr.data > key and succ is None:
            succ = curr
            break

        prev = curr
        curr = curr.right

    return pred, succ


# ─────────────────────────────────────────────────────────────────────────────
# ✅ Approach 3 — two BST-guided walks, no traversal (optimal)
#
# Exploit BST ordering directly — same structure as floorBST/ceilBST but with
# STRICT inequalities (< and >) instead of <= and >=.
#
# Successor walk (smallest value > key):
#   node.data > key  → candidate; go LEFT to find something smaller but still > key
#   node.data <= key → too small or equal; go RIGHT
#
# Predecessor walk (largest value < key):
#   node.data < key  → candidate; go RIGHT to find something larger but still < key
#   node.data >= key → too large or equal; go LEFT
#
# O(h) time, O(1) space.
# ─────────────────────────────────────────────────────────────────────────────
def predecessorSuccessor_v3(root, key):
    predecessor, successor = None, None

    # find successor: smallest value strictly > key
    node = root
    while node:
        if node.data > key:
            successor = node        # candidate; look for something smaller on the left
            node = node.left
        else:
            node = node.right       # node.data <= key → skip, go right

    # find predecessor: largest value strictly < key
    node = root
    while node:
        if node.data < key:
            predecessor = node      # candidate; look for something larger on the right
            node = node.right
        else:
            node = node.left        # node.data >= key → skip, go left

    return predecessor, successor


# ─────────────────────────────────────────────────────────────────────────────
# Why predecessor/successor differs from floor/ceil by just one symbol:
#
#   floor  uses  node.data <= key  (key itself counts as a floor candidate)
#   pred   uses  node.data <  key  (key itself is excluded → strict)
#
#   ceil   uses  node.data >= key  (key itself counts as a ceil candidate)
#   succ   uses  node.data >  key  (key itself is excluded → strict)
#
# Changing <= to < / >= to > is the entire algorithmic difference.
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    test_cases = [
        ([8, 4, 12, 2, 6, 10, 14], 8,  (6,   10)),
        ([8, 4, 12, 2, 6, 10, 14], 11, (10,  12)),
        ([8, 4, 12, 2, 6, 10, 14], 15, (14,  None)),
        ([8, 4, 12, 2, 6, 10, 14], 1,  (None, 2)),
        ([8, 4, 12, 2, 6, 10, 14], 4,  (2,    6)),
        ([5],                        5,  (None, None)),
    ]

    for fn_name, fn in [("v1 brute", predecessorSuccessor_v1),
                        ("v2 inorder", predecessorSuccessor_v2),
                        ("v3 optimal", predecessorSuccessor_v3)]:
        print(f"\n── {fn_name} ──")
        for vals, key, (exp_pred, exp_succ) in test_cases:
            root = build_bst(vals)
            pred, succ = fn(root, key)
            pred_val = pred.data if pred else None
            succ_val = succ.data if succ else None
            status = "✅" if (pred_val, succ_val) == (exp_pred, exp_succ) else "❌"
            print(f"  {status} key={key:2d} → pred={pred_val}, succ={succ_val}  (expected {exp_pred}, {exp_succ})")
