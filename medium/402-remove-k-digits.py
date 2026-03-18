"""
LeetCode 402. Remove K Digits  |  Medium

Given a number string and integer k, remove k digits to make the smallest
possible number. Return it as a string with no leading zeros ("0" if empty).

Examples:
    "1432219", k=3 → "1219"   (remove 4,3,2)
    "10200",   k=1 → "200"    (remove 1, strip leading zero)
    "10",      k=2 → "0"      (remove all → "0")
"""


# ─────────────────────────────────────────────────────────────────────────────
# SOLUTION: Monotonic Stack (Greedy)
# Time  : O(n),  Space : O(n)
#
# Greedy insight:
#   To make the number as small as possible, we want digits in INCREASING order.
#   Whenever a new digit is SMALLER than the stack top, the stack top is a
#   "peak" — removing it shrinks the number. So pop it (spend one removal).
#
# Algorithm:
#   1. Iterate through each digit ch in num.
#      While stack is non-empty AND stack top > ch AND k > 0:
#        pop stack top (remove that digit), decrement k
#      Push ch onto stack.
#
#   2. If k > 0 after the loop (number was non-decreasing, no early pops used):
#      Remove from the END (largest digits are at the tail of a sorted sequence).
#
#   3. Strip leading zeros, return "0" if empty.
#
# Trace for "1432219", k=3:
#   ch=1: stack=[]           → push → [1]
#   ch=4: 4 > 1? No pop      → push → [1,4]
#   ch=3: 4 > 3 → pop 4 (k=2) → 1 < 3? stop → push → [1,3]
#   ch=2: 3 > 2 → pop 3 (k=1) → 1 < 2? stop → push → [1,2]
#   ch=2: stack top=2, not > 2 → push → [1,2,2]
#   ch=1: 2 > 1 → pop 2 (k=0) → k=0, stop → push → [1,2,1]
#   ch=9: k=0, no pops       → push → [1,2,1,9]
#   k=0, no tail removal
#   result = "1219"  ✓
#
# Trace for "10200", k=1:
#   ch=1: push → [1]
#   ch=0: 1 > 0 → pop 1 (k=0) → push → [0]
#   ch=2: push → [0,2]
#   ch=0: push → [0,2,0]
#   ch=0: push → [0,2,0,0]
#   strip leading zero → "200"  ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def removeKdigits(self, num, k):
        stack = []

        for ch in num:
            # pop larger digits while we still have removals left
            while stack and stack[-1] > ch and k > 0:
                stack.pop()
                k -= 1
            stack.append(ch)

        # if k > 0, the number was non-decreasing — remove from the tail
        while k > 0:
            stack.pop()
            k -= 1

        # strip leading zeros
        i = 0
        while i < len(stack) and stack[i] == "0":
            i += 1

        result = "".join(stack[i:])     # or: ''.join(stack).lstrip('0')

        return result if result else "0"
