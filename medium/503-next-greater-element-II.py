"""
LeetCode 503. Next Greater Element II  |  Medium

Given a CIRCULAR integer array, return the next greater element for every
element. Search wraps around the end. Return -1 if none exists.

Examples:
    [1,2,1]     → [2,-1,2]
    [1,2,3,4,3] → [2,3,4,-1,4]
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Brute Force
# Time  : O(n²),  Space : O(1)
#
# For each element at index i, scan forward up to n-1 more positions
# (wrapping with % n) to find the first greater element.
# ─────────────────────────────────────────────────────────────────────────────
def nextGreaterElements_brute(nums):
    n = len(nums)
    res = [-1] * n

    for i in range(n):
        for j in range(1, n):               # search up to n-1 positions ahead
            nxt = nums[(i + j) % n]         # wrap around using modulo
            if nxt > nums[i]:
                res[i] = nxt
                break                       # first greater found → stop

    return res


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: Monotonic Stack with 2n simulation  ← OPTIMAL
# Time  : O(n),  Space : O(n)
#
# Core trick — simulate the circular array by iterating 2*n times (0 to 2n-1)
# and using i % n to wrap indices back into [0, n-1].
#
# Why 2n works:
#   In a circular array, any element's next greater is at most n-1 steps ahead.
#   Two full passes guarantees every element has "seen" all elements after it.
#   We only PUSH to the stack in the first pass (i < n) — the second pass
#   only resolves any remaining unmatched elements.
#
# Stack holds (value, original_index) pairs in DECREASING order.
# When cur > stack top, cur is the next greater for that top element.
#
# Trace: nums = [1, 6, 3, 4],  n=4
#   i=0: cur=1 → stack=[(1,0)]
#   i=1: cur=6 > 1 → pop (1,0), res[0]=6  → stack=[(6,1)]
#   i=2: cur=3 < 6 → stack=[(6,1),(3,2)]
#   i=3: cur=4 > 3 → pop (3,2), res[2]=4  → 4 < 6 → stack=[(6,1),(4,3)]
#   i=4: cur=nums[0]=1 < 4 → nothing (i≥n, don't push)
#   i=5: cur=nums[1]=6 = 6, not > 6 → nothing
#   i=6: cur=nums[2]=3 < 4 → nothing
#   i=7: cur=nums[3]=4 = 4, not > stack top → nothing
#   Remaining stack: [(6,1),(4,3)] → res[1]=-1, res[3]=-1
#   res = [6, -1, 4, -1]  ✓
# ─────────────────────────────────────────────────────────────────────────────
def nextGreaterElements(nums):
    res = [-1] * len(nums)
    stack = []                  # stores (value, index), decreasing from bottom to top
    n = len(nums)

    for i in range(2 * n):     # two full passes to cover circular lookups
        cur = nums[i % n]       # wrap index for second pass

        # cur is greater than top → it's the next greater for popped elements
        while stack and cur > stack[-1][0]:
            val, j = stack.pop()
            res[j] = cur        # record answer for original index j

        if i < n:               # only push during the FIRST pass
            stack.append([cur, i])

    return res
