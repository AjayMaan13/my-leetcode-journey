"""
LeetCode 496. Next Greater Element I  |  Easy

For each element in nums1, find the first greater element to its RIGHT
in nums2. Return -1 if none exists. nums1 is a subset of nums2.

Examples:
    nums1=[4,1,2], nums2=[1,3,4,2] → [-1, 3, -1]
    nums1=[2,4],   nums2=[1,2,3,4] → [3, -1]
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Brute Force — scan right for each element
# Time  : O(m * n),  Space : O(n)
#
# For every element in nums2, walk rightward until a greater value is found.
# Store results in a hashmap, then look up each nums1 element.
# ─────────────────────────────────────────────────────────────────────────────
def nextGreaterElement_brute(nums1, nums2):
    if not nums1 or not nums2:
        return []

    nextG = {}

    for i in range(len(nums2) - 1, -1, -1):
        num = nums2[i]
        g = -1
        j = i + 1
        while g == -1 and j < len(nums2):   # scan right until greater found
            if nums2[j] > num:
                g = nums2[j]
            j += 1
        nextG[num] = g

    return [nextG[num] for num in nums1]


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: Monotonic Stack  ← OPTIMAL
# Time  : O(m + n),  Space : O(n)
#
# Key insight — use a DECREASING monotonic stack:
#   Iterate left → right through nums2.
#   The stack holds elements "waiting" for their next greater element.
#   When we see a new element `cur`:
#     → it is the next greater for everything in the stack that is SMALLER.
#     → pop those elements and record `cur` as their answer.
#     → push `cur` onto the stack (it's now waiting for ITS next greater).
#
# We only push elements that exist in nums1 (via next1Idx lookup),
# since we only need answers for nums1 elements.
#
# Trace: nums1=[4,1,2], nums2=[1,3,4,2]
#   next1Idx = {4:0, 1:1, 2:2}   (value → index in nums1)
#   res = [-1, -1, -1]
#
#   cur=1: stack=[]  → nothing to pop; 1 in next1Idx → push 1  → stack=[1]
#   cur=3: 3 > 1     → pop 1, res[1]=3  → stack=[]; 3 not in next1Idx → skip
#   cur=4: stack=[]  → nothing to pop; 4 in next1Idx → push 4  → stack=[4]
#   cur=2: 2 < 4     → nothing to pop; 2 in next1Idx → push 2  → stack=[4,2]
#   end: remaining stack elements [4,2] never got a greater → stay -1
#
#   res = [-1, 3, -1]  ✓
#
# Why monotonic stack works:
#   The stack always holds values in DECREASING order (top is smallest).
#   A new larger value "resolves" all smaller waiting values in one sweep.
#   Each element is pushed and popped at most once → O(n) total.
# ─────────────────────────────────────────────────────────────────────────────
def nextGreaterElement(nums1, nums2):
    if not nums1 or not nums2:
        return []

    next1Idx = {n: i for i, n in enumerate(nums1)}  # value → its index in nums1
    res = [-1] * len(nums1)                          # default answer is -1

    stack = []                                       # monotonic decreasing stack
    for i in range(len(nums2)):
        cur = nums2[i]

        # cur is greater than stack top → it's the next greater for those elements
        while stack and cur > stack[-1]:
            val = stack.pop()
            idx = next1Idx[val]     # where does this value sit in nums1?
            res[idx] = cur          # record cur as its next greater element

        # only track elements that appear in nums1 (others don't need answers)
        if cur in next1Idx:
            stack.append(cur)

    return res
