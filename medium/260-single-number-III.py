"""
LeetCode 260. Single Number III  |  Medium

Problem:
Given an integer array where exactly two elements appear only once and all
others appear exactly twice, find the two unique elements.
Must be O(N) time and O(1) space.

Examples:
    [1,2,1,3,2,5] → [3, 5]
    [-1, 0]       → [-1, 0]
    [0, 1]        → [1, 0]
"""


# ─────────────────────────────────────────────────────────────────────────────
# MY SOLUTION: XOR + Bit Partition
# Time  : O(N),  Space : O(1)
#
# Step 1 — XOR everything together.
#   Duplicates cancel (a ^ a = 0), leaving xor_all = a ^ b
#   (the XOR of the two unique numbers).
#
# Step 2 — Find a bit where a and b DIFFER.
#   xor_all has a 1-bit wherever a and b differ.
#   We grab the RIGHTMOST set bit using: rightmostBit = xor_all & (-xor_all)
#
#   Why -xor_all works (two's complement trick):
#     -x = ~x + 1  →  flips all bits then adds 1
#     The add-1 carries through all the trailing 1s, flipping them back to 0,
#     until it hits the first 0 (which was a 1 in x) and sets it.
#     Result: only the lowest set bit of x survives the AND.
#
#     e.g. xor_all = 6  →  binary 110
#          -xor_all     →  binary 010  (two's complement)
#          6 & -6       →  010  →  rightmostBit = 2  (bit position 1)
#
# Step 3 — Partition nums into two groups by that bit, XOR each group.
#   Every number goes into exactly one group (bit is set or not).
#   Within each group, duplicates cancel → only the unique number survives.
#   Group 1 (bit SET)   → produces `a`
#   Group 2 (bit UNSET) → produces `b`
#
#   e.g. nums = [1,2,1,3,2,5], xor_all = 3^5 = 6 (110), rightmostBit = 2 (010)
#     bit set   (& 2 != 0): 2, 3, 2  →  2^3^2 = 3  ✓
#     bit unset (& 2 == 0): 1, 1, 5  →  1^1^5 = 5  ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def singleNumber(self, nums):
        xor_all = 0
        for num in nums:
            xor_all ^= num              # Step 1: xor_all = a ^ b

        rightmostBit = xor_all & (-xor_all)  # Step 2: isolate lowest differing bit

        a, b = 0, 0
        for num in nums:                # Step 3: partition and XOR each group
            if num & rightmostBit:
                a ^= num
            else:
                b ^= num

        return [a, b]
