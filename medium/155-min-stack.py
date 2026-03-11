"""
LeetCode 155. Min Stack  |  Medium

Design a stack supporting push, pop, top, and getMin — all in O(1) time.

Example:
    push(-2), push(0), push(-3)
    getMin() → -3
    pop()
    top()    → 0
    getMin() → -2
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Two Stacks
# Time  : O(1) all ops,  Space : O(N)
#
# Use two stacks in parallel:
#   stack     — stores all pushed values (normal stack behaviour)
#   min_stack — stores the current minimum AT EACH LEVEL
#
# Every push adds to both stacks.
# min_stack always keeps track of "what is the min if I pop down to here?"
#
# Trace: push(-2), push(0), push(-3)
#   stack:     [-2, 0, -3]
#   min_stack: [-2, -2, -3]   ← after push(0), min is still -2; after push(-3), min is -3
#
#   getMin() → min_stack top = -3  ✓
#   pop()    → remove from both → stack[-2,0], min_stack[-2,-2]
#   getMin() → min_stack top = -2  ✓
# ─────────────────────────────────────────────────────────────────────────────
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []         # parallel stack tracking running minimum

    def push(self, val: int) -> None:
        self.stack.append(val)
        # new min is val if stack was empty or val is smaller than current min
        if not self.min_stack:
            self.min_stack.append(val)
        else:
            self.min_stack.append(min(val, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()        # keep both stacks in sync

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]   # top of min_stack = current minimum


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: Stack of Pairs  ← CLEANER
# Time  : O(1) all ops,  Space : O(N)
#
# Instead of two separate stacks, store (value, current_min) as a pair
# in a single stack. Each entry carries its own "snapshot" of the min.
#
# Same idea as Approach 1 but expressed more cleanly — one data structure
# instead of two, harder to accidentally desync.
#
# Trace: push(-2), push(0), push(-3)
#   stack: [(-2, -2), (0, -2), (-3, -3)]
#            val  min   val  min   val  min
#
#   getMin() → stack[-1][1] = -3  ✓
#   pop()    → stack becomes [(-2,-2),(0,-2)]
#   getMin() → stack[-1][1] = -2  ✓
# ─────────────────────────────────────────────────────────────────────────────
class MinStack:
    def __init__(self):
        self.stack = []             # each entry: (value, current_min_at_this_level)

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append((val, val))           # first element, min is itself
        else:
            current_min = self.stack[-1][1]
            self.stack.append((val, min(val, current_min)))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]    # first element of pair = value

    def getMin(self) -> int:
        return self.stack[-1][1]    # second element of pair = min at this level
