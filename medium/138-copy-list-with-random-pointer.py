"""
LeetCode 138. Copy List with Random Pointer  |  Medium

A linked list of length n is given such that each node contains an additional
random pointer, which could point to any node in the list, or null.

Construct a deep copy of the list. The deep copy should consist of exactly n
brand new nodes, where each new node has its value set to the value of its
corresponding original node. Both the next and random pointers of the new
nodes should point to new nodes in the copied list such that the pointers in
the original list and copied list represent the same list state. None of the
pointers in the new list should point to nodes in the original list.

Examples:
    Input:  [[7,null],[13,0],[11,4],[10,2],[1,0]]
    Output: [[7,null],[13,0],[11,4],[10,2],[1,0]]

    Input:  [[1,1],[2,1]]
    Output: [[1,1],[2,1]]

    Input:  [[3,null],[3,0],[3,null]]
    Output: [[3,null],[3,0],[3,null]]

Constraints:
    0 <= n <= 1000
    -10^4 <= Node.val <= 10^4
    Node.random is null or points to some node in the linked list.
"""


class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: HASHMAP — Two Pass  (your original solution, cleaned up)
# Time  : O(n)
# Space : O(n)  — hashmap stores a mapping for every node
#
# Idea:
#   Pass 1 — create a clone node for every original node, store in a dict.
#   Pass 2 — wire up .next and .random on each clone using the dict.
#
# The {None: None} seed means we never need a None-check inside the loop.
# ─────────────────────────────────────────────────────────────────────────────
class Solution1:
    def copyRandomList(self, head: Node) -> Node:
        old_to_new = {None: None}   # seed so None lookups work for free

        # Pass 1: clone every node (value only)
        curr = head
        while curr:
            old_to_new[curr] = Node(curr.val)
            curr = curr.next

        # Pass 2: wire next and random using the map
        curr = head
        while curr:
            clone = old_to_new[curr]
            clone.next   = old_to_new[curr.next]
            clone.random = old_to_new[curr.random]
            curr = curr.next

        return old_to_new[head]


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: HASHMAP — Single Pass  (slightly fewer lines, same complexity)
# Time  : O(n)
# Space : O(n)
#
# Idea:
#   Build clones lazily — the first time we see a node (via .next or .random)
#   we create it on the spot and cache it. One pass covers everything.
# ─────────────────────────────────────────────────────────────────────────────
class Solution2:
    def copyRandomList(self, head: Node) -> Node:
        if not head:
            return None

        cache = {}

        def clone(node):
            """Return cached clone, or create + cache a new one."""
            if node is None:
                return None
            if node not in cache:
                cache[node] = Node(node.val)   # create clone (links set later)
            return cache[node]

        curr = head
        while curr:
            clone(curr).next   = clone(curr.next)    # wire next
            clone(curr).random = clone(curr.random)  # wire random
            curr = curr.next

        return clone(head)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: INTERWEAVING  ← best overall (same runtime, O(1) extra space)
# Time  : O(n)  — three linear passes
# Space : O(1)  — no hashmap; uses the list itself as a lookup table
#
# Idea (three passes):
#   Pass 1 — Interweave: insert each clone right after its original.
#             1 -> 1' -> 2 -> 2' -> 3 -> 3' -> ...
#
#   Pass 2 — Random pointers: because clone(X) == X.next, we can set
#             X.next.random = X.random.next  (no map needed)
#
#   Pass 3 — Separate: restore the original list and extract the clone list.
# ─────────────────────────────────────────────────────────────────────────────
class Solution3:
    def copyRandomList(self, head: Node) -> Node:
        if not head:
            return None

        # ─────────────────────────────────────────────────────────────
        # PASS 1 — INTERWEAVE: insert each clone right after its original
        #
        # Before:
        #   1  ->  2  ->  3  ->  None
        #
        # After:
        #   1  ->  1' ->  2  ->  2' ->  3  ->  3' ->  None
        #
        # Why? Once interleaved, clone(X) is always just X.next
        # so we never need a hashmap to look up "who is X's clone"
        # ─────────────────────────────────────────────────────────────
        curr = head
        while curr:
            clone      = Node(curr.val)   # new node, value only
            clone.next = curr.next        # clone skips ahead to original's next
            curr.next  = clone            # original now points to clone
            curr       = clone.next       # jump over clone to next original

        # ─────────────────────────────────────────────────────────────
        # PASS 2 — RANDOM POINTERS: wire .random on every clone
        #
        # Key insight (no map needed):
        #   clone of X     = X.next
        #   clone of X.random = X.random.next
        #
        # Example — if original node A has A.random -> C:
        #
        #   A  ->  A' ->  B  ->  B' ->  C  ->  C'
        #   |                           |
        #   random                      random (original)
        #
        #   So:  A'.random = A.random.next = C.next = C'  ✓
        # ─────────────────────────────────────────────────────────────
        curr = head
        while curr:
            if curr.random:
                curr.next.random = curr.random.next  # clone's random = clone of original's random
            # curr.next is the clone, curr.next.next is the next original
            curr = curr.next.next

        # ─────────────────────────────────────────────────────────────
        # PASS 3 — SEPARATE: split the interleaved list back into two
        #
        # Starting state (interleaved):
        #   1  ->  1' ->  2  ->  2' ->  3  ->  3' ->  None
        #   ^orig          ^orig          ^orig
        #         ^clone         ^clone         ^clone
        #
        # Goal — restore original:   1  ->  2  ->  3  ->  None
        #         extract clone  :   1' ->  2' ->  3' ->  None
        #
        # Step-by-step for each iteration:
        #
        #  curr = 1  (original node)
        #  ┌─────────────────────────────────────────────────────┐
        #  │ Before:  ... 1 -> 1' -> 2 -> 2' -> 3 -> 3' -> None │
        #  │                                                      │
        #  │  clone_node  = curr.next        →  1'               │
        #  │  curr.next   = clone_node.next  →  1.next  = 2  ✓   │
        #  │  clone_tail.next = clone_node   →  dummy -> 1'      │
        #  │  clone_tail  = clone_node       →  tail now at 1'   │
        #  │  curr        = curr.next        →  advance to 2     │
        #  └─────────────────────────────────────────────────────┘
        #
        #  curr = 2
        #  ┌─────────────────────────────────────────────────────┐
        #  │  clone_node  = 2'                                   │
        #  │  curr.next   = 3              (2.next restored)     │
        #  │  clone_tail.next = 2'         (1' -> 2')            │
        #  │  clone_tail  = 2'                                   │
        #  │  curr        = 3                                    │
        #  └─────────────────────────────────────────────────────┘
        #
        #  curr = 3
        #  ┌─────────────────────────────────────────────────────┐
        #  │  clone_node  = 3'                                   │
        #  │  curr.next   = None           (3.next restored)     │
        #  │  clone_tail.next = 3'         (2' -> 3')            │
        #  │  clone_tail  = 3'                                   │
        #  │  curr        = None  → loop ends                    │
        #  └─────────────────────────────────────────────────────┘
        #
        # Final state:
        #   Original (restored):  1  ->  2  ->  3  ->  None
        #   Clone list         :  1' ->  2' ->  3' ->  None   ← we return this
        # ─────────────────────────────────────────────────────────────
        dummy      = Node(0)      # throwaway head for the clone list
        clone_tail = dummy        # pointer that grows the clone list

        curr = head
        while curr:
            clone_node       = curr.next          # grab the clone sitting next to curr
            curr.next        = clone_node.next    # stitch original list back together
            clone_tail.next  = clone_node         # append clone to clone list
            clone_tail       = clone_node         # advance clone list tail
            curr             = curr.next          # advance in the (now restored) original

        return dummy.next   # skip the throwaway head → first real clone node

