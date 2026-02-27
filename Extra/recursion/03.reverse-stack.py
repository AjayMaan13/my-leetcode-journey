"""
Reverse a Stack Using Recursion  |  TUF Problem

Problem Statement:
    Given a stack of integers, reverse it using recursion.
    Only standard stack ops allowed: push(), pop(), peek/top, isEmpty().
    No loops, no extra data structures. Modify the stack in-place.

    Convention:
      - List's RIGHT end = TOP of stack  (stack[-1] is top)
      - List's LEFT end  = BOTTOM of stack

Examples:
    [4, 1, 3, 2]         →  [2, 3, 1, 4]
    [10, 20, -5, 7, 15]  →  [15, 7, -5, 20, 10]

Key Insight — two recursive functions working together:

    reverse_stack     : peels off the top one at a time, reverses the rest,
                        then inserts the peeled element at the BOTTOM.

    insert_at_bottom  : to insert X at the bottom of a stack, pop everything
                        off, push X, then push everything back.

    Together they do what you cannot do with one function alone — you have
    no direct access to the bottom of a stack, so you have to "simulate" it
    by temporarily emptying and refilling.
"""


# ─────────────────────────────────────────────────────────────────────────────
# HELPER: insert_at_bottom
# Time  : O(n)  — must pop everything to reach bottom, then push back
# Space : O(n)  — recursion depth = current stack size
#
# Goal: push `val` at the very BOTTOM of the stack (index 0),
#       leaving everything else in the same order above it.
#
# Visual trace for insert_at_bottom([1,3,2], val=4):
# (right = top, so stack looks like: bottom[1,3,2]top)
#
#   pop 2  →  insert_at_bottom([1,3], 4)
#     pop 3  →  insert_at_bottom([1], 4)
#       pop 1  →  insert_at_bottom([], 4)
#         stack empty → push 4       stack: [4]       ← val now at bottom
#       push 1 back                  stack: [4,1]
#     push 3 back                    stack: [4,1,3]
#   push 2 back                      stack: [4,1,3,2]  ✓  (4 is now at bottom)
# ─────────────────────────────────────────────────────────────────────────────
def insert_at_bottom(stack: list, val: int) -> None:
    if not stack:
        # Base case: stack is empty → val becomes the only element (at bottom)
        stack.append(val)
        return

    # Pop top to get it out of the way
    top = stack.pop()

    # Recurse — keep popping until empty, then val gets pushed at the base
    insert_at_bottom(stack, val)

    # Restore top above val (and everything already re-pushed below)
    stack.append(top)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN: reverse_stack
# Time  : O(n^2)  — reverse_stack is O(n) calls, each calls insert_at_bottom
#                   which is O(n) → total O(n^2)
# Space : O(n)    — max recursion depth = n (two stacks of depth n each,
#                   but they don't overlap, so O(n) at any point in time)
#
# Goal: reverse the stack in-place using only recursion + push/pop.
#
# Idea:
#   1. Pop the top element (call it `top`)
#   2. Recursively reverse everything below it
#   3. Insert `top` at the BOTTOM of the now-reversed stack
#
# Why does this work?
#   If stack = [4, 1, 3, 2]  (2 is on top):
#     We want result = [2, 3, 1, 4]  (4 on top after reverse? No —
#     reverse means 4 goes to bottom, 2 comes to top)
#
#   reverse_stack([4,1,3,2]):
#     pop 2
#     reverse_stack([4,1,3]):
#       pop 3
#       reverse_stack([4,1]):
#         pop 1
#         reverse_stack([4]):
#           pop 4
#           reverse_stack([])  → base case, return
#           insert_at_bottom([], 4)  → [4]
#         insert_at_bottom([4], 1)   → [1,4]    (1 at bottom, 4 on top)
#       insert_at_bottom([1,4], 3)   → [1,3,4]  (3 inserted above 1, below 4... wait)
#
# Let me re-trace more carefully. After reverse_stack([4,1,3]) returns:
#   The sub-stack [4,1,3] should become [3,1,4].
#   Then insert_at_bottom([3,1,4], 2) → [2,3,1,4]
#   top of [2,3,1,4] = 4  ← which was originally at the bottom ✓
#
# Full trace (right=top):
#   reverse_stack([4,1,3,2])
#     pop 2
#     reverse_stack([4,1,3])
#       pop 3
#       reverse_stack([4,1])
#         pop 1
#         reverse_stack([4])
#           pop 4
#           reverse_stack([]) → return
#           insert_at_bottom([], 4)  → stack=[4]
#         insert_at_bottom([4], 1)
#           pop 4, insert_at_bottom([], 1) → push 1 → [1], push 4 back → [1,4]
#       insert_at_bottom([1,4], 3)
#         pop 4, insert_at_bottom([1],3)
#           pop 1, insert_at_bottom([],3) → push 3 → [3], push 1 → [3,1]
#         push 4 → [3,1,4]
#     insert_at_bottom([3,1,4], 2)
#       pop 4, insert_at_bottom([3,1],2)
#         pop 1, insert_at_bottom([3],2)
#           pop 3, insert_at_bottom([],2) → push 2 → [2], push 3 → [2,3]
#         push 1 → [2,3,1]
#       push 4 → [2,3,1,4]   ✓  (top=4, which was originally at bottom)
# ─────────────────────────────────────────────────────────────────────────────
def reverse_stack(stack: list) -> None:
    # Base case: empty or single element — already reversed
    if not stack:
        return

    # Step 1: remove the top element
    top = stack.pop()

    # Step 2: recursively reverse everything remaining
    reverse_stack(stack)

    # Step 3: put the removed top at the BOTTOM of the now-reversed stack
    # (it was on top originally, so it belongs at the bottom after reversal)
    insert_at_bottom(stack, top)

