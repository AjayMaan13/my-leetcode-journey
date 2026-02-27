"""
Sort a Stack  |  TUF Problem

Problem Statement:
    Given a stack of integers, sort it in descending order using recursion
    such that the TOP of the stack contains the GREATEST element.

    Rules:
      - Only use recursive operations
      - Only use standard stack ops: push(), pop(), peek/top, isEmpty()
      - No loop-based sorting (quicksort, mergesort, etc.)

    Convention used throughout this file:
      - List's RIGHT end  = TOP of stack  (stack[-1] is top)
      - List's LEFT end   = BOTTOM of stack
      - Correct sorted output = [smallest, ..., greatest]
                                                       ^ top

Examples:
    Input:  [4, 1, 3, 2]       →  Output: [1, 2, 3, 4]   (4 is on top)
    Input:  [1]                →  Output: [1]
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: CHEATING SOLUTION (your worst one — honest label kept)
# Time  : O(n^2 log n)  — sorted() called at every recursion level
# Space : O(n)          — recursion depth = n
#
# Violates the spirit of the problem:
#   - Does NOT use push/pop at all
#   - Calls Python's built-in sorted() which is O(n log n) per level
#
# Bug in your original: sorted(reverse=True) puts greatest at index 0 = bottom,
# meaning SMALLEST ends up on top — opposite of what we want.
# Fixed here to sorted(reverse=False) so greatest stays at [-1] = top.
# ─────────────────────────────────────────────────────────────────────────────
def sortStack_cheat(stack: list) -> list:
    if not stack:
        return []

    def recSortStack(items):
        if len(items) == 1:
            return items
        res = recSortStack(items[1:])
        res.append(items[0])
        res = sorted(res)               # ascending: greatest at [-1] = top ✓
        return res

    return recSortStack(stack)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: RECURSIVE INSERTION SORT — nested helper  (your clean version)
# Time  : O(n^2)  — sortS() makes n calls, each insertS() call is O(n)
# Space : O(n)    — two recursion stacks (sortS + insertS), both depth n
#
# Two functions work together like insertion sort on a stack:
#
#   sortS   — recursively strips the stack down to empty, then re-inserts
#             each element in sorted order on the way back up
#
#   insertS — places one element into its correct spot in an already-sorted
#             stack (greatest on top), using only push/pop
#
# ── insertS logic ───────────────────────────────────────────────────────────
# We want greatest at TOP (items[-1]). When inserting `item`:
#
#   Case A: stack empty OR item >= top
#           → item belongs ON TOP of whatever is there → just push
#
#   Case B: item < top
#           → top is GREATER than item, so top must stay above item.
#             Pop top temporarily, recurse to find item's spot below,
#             then push top back so it ends up above item.
#
# Visual trace — insertS building [1,2,3,4] one element at a time:
#
#   insertS(4, [])    →  []   → push 4        →  [4]
#   insertS(1, [4])   →  1 < 4 (Case B)
#                           pop 4, insertS(1,[])
#                           → push 1           → [1]
#                           push 4 back        → [1,4]
#   insertS(3, [1,4]) →  3 < 4 (Case B)
#                           pop 4, insertS(3,[1])
#                           → 3 >= 1 (Case A)  → push 3  → [1,3]
#                           push 4 back        → [1,3,4]
#   insertS(2, [1,3,4])→ 2 < 4 (Case B)
#                           pop 4, insertS(2,[1,3])
#                           → 2 < 3 (Case B)
#                             pop 3, insertS(2,[1])
#                             → 2 >= 1 (Case A) → push 2 → [1,2]
#                             push 3 back        → [1,2,3]
#                           push 4 back          → [1,2,3,4]  ✓
#
# ── sortS logic ─────────────────────────────────────────────────────────────
# sortS([4,1,3,2]):
#   pop 2 → sortS([4,1,3])
#     pop 3 → sortS([4,1])
#       pop 1 → sortS([4])
#         pop 4 → sortS([])  → []
#         insertS(4, [])    → [4]
#       insertS(1, [4])     → [1,4]
#     insertS(3, [1,4])     → [1,3,4]
#   insertS(2, [1,3,4])     → [1,2,3,4]  ✓
# ─────────────────────────────────────────────────────────────────────────────
def sortStack_nested(stack: list) -> list:
    if not stack:
        return []

    def insertS(item, items):
        if not items or item >= items[-1]:
            # Stack empty, OR item is >= top → item belongs on top
            items.append(item)
        else:
            # item < top → top must stay ABOVE item
            # Temporarily remove top, find item's spot, restore top
            temp = items.pop()
            insertS(item, items)
            items.append(temp)      # temp goes back on top (temp > item ✓)
        return items

    def sortS(items):
        if not items:
            return []
        element = items.pop()           # take top element off
        res = sortS(items)              # sort the rest recursively
        return insertS(element, res)    # insert element into correct position

    return sortS(stack)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: RECURSIVE INSERTION SORT — flat (your compact version)
# Time  : O(n^2)
# Space : O(n)
#
# Same logic as Approach 2 but without a wrapper function.
# sortStack_flat calls itself directly and mutates the list in-place.
# ─────────────────────────────────────────────────────────────────────────────
def _insertS(item: int, items: list) -> list:
    """Insert item into sorted stack, maintaining greatest at top."""
    if not items or item >= items[-1]:
        items.append(item)
    else:
        temp = items.pop()
        _insertS(item, items)
        items.append(temp)
    return items

def sortStack_flat(stack: list) -> list:
    if not stack:
        return []
    element = stack.pop()               # pop top
    sortStack_flat(stack)               # sort remaining stack in-place
    return _insertS(element, stack)     # insert element into correct position


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: AUXILIARY STACK — iterative (bonus, not recursive)
# Time  : O(n^2)
# Space : O(n)  — one extra stack
#
# Classic textbook approach using only push/pop with a helper stack.
# Not recursive, but the cleanest to trace through mentally.
#
# Visual trace for [4,1,3,2]  (right = top):
#
#   input=[4,1,3,2]  aux=[]
#   ┌─────────────────────────────────────────────────────┐
#   │ pop 2: aux empty       → push 2      aux=[2]        │
#   │ pop 3: aux top=2 < 3   → push 3      aux=[2,3]      │
#   │ pop 1: aux top=3 > 1   → move 3 back                │
#   │        aux top=2 > 1   → move 2 back                │
#   │        aux empty       → push 1      aux=[1]        │
#   │        push 2,3 back   → aux=[1,2,3]                │
#   │ pop 4: aux top=3 < 4   → push 4      aux=[1,2,3,4]  │
#   └─────────────────────────────────────────────────────┘
#   Result: [1,2,3,4]  top=4 ✓
# ─────────────────────────────────────────────────────────────────────────────
def sortStack_auxiliary(stack: list) -> list:
    if not stack:
        return []

    aux = []

    while stack:
        curr = stack.pop()

        # curr is smaller than aux top → curr must go BELOW aux top
        # Keep moving aux elements back until we find curr's correct spot
        while aux and aux[-1] > curr:
            stack.append(aux.pop())

        aux.append(curr)    # curr is now in the right position

    return aux   # greatest at aux[-1] = top ✓
