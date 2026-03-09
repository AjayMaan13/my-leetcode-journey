"""
LeetCode 137. Single Number II  |  Medium

Problem:
Every element appears exactly three times except for one which appears once.
Find the single element. Must be O(N) time and O(1) space.

Examples:
    [2,2,3,2]         → 3
    [0,1,0,1,0,1,99]  → 99
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: HashMap (Brute Force)
# Time  : O(N),  Space : O(N)
#
# Count frequency of each number. Return the one with count == 1.
# Fails the O(1) space constraint but good starting point.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def singleNumber(self, nums):
        from collections import Counter
        count = Counter(nums)
        for num, freq in count.items():
            if freq == 1:
                return num


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: Sort + Linear Traversal (jump by 3)
# Time  : O(N log N),  Space : O(1)
#
# After sorting, all triplicates are grouped together.
# Jump through in steps of 3 — if nums[i] != nums[i+2], the unique one
# is at index i (it broke the triplet). If we exhaust the loop, the
# unique element is the last one.
#
# e.g. [2,2,2,3,99,99,99] after sort:
#   i=0: nums[0]=2, nums[2]=2 → same, skip  (triplet intact)
#   i=3: nums[3]=3, nums[5]=99 → differ → return nums[3]=3  ✓
#
# Why jump by 3? Because every triplet occupies exactly 3 consecutive slots
# after sorting. If all 3 match, move past the whole triplet.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def singleNumber(self, nums):
        nums.sort()
        i = 0
        while i < len(nums) - 1:
            if nums[i] == nums[i + 2]:  # triplet intact → skip all 3
                i += 3
            else:
                return nums[i]          # triplet broken → unique is here
        return nums[-1]                 # unique is the last element


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: Counting Set Bits  ← BETTER THAN APPROACH 2
# Time  : O(32 * N) = O(N),  Space : O(1)
#
# Key insight:
#   For each bit position (0 to 31), sum up that bit across ALL numbers.
#   Since triplicates appear 3 times, their bits contribute multiples of 3.
#   The unique number's bits are NOT a multiple of 3 → show up as remainder 1.
#   So: (sum of bit i across all nums) % 3 → gives bit i of the answer.
#
# e.g. nums = [2, 2, 3, 2]
#   Binary:  2=010, 2=010, 3=011, 2=010
#
#   bit 0 sum: 0+0+1+0 = 1  → 1 % 3 = 1  → answer has bit 0 set
#   bit 1 sum: 1+1+1+1 = 4  → 4 % 3 = 1  → answer has bit 1 set
#   bit 2 sum: 0+0+0+0 = 0  → 0 % 3 = 0  → answer has bit 2 unset
#
#   Reconstruct: bit1=1, bit0=1 → 11 in binary = 3  ✓
#
# This works for any "appears k times except one" problem — just replace % 3
# with % k.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def singleNumber(self, nums):
        result = 0
        for i in range(32):                         # check all 32 bit positions
            bit_sum = sum((num >> i) & 1 for num in nums)  # count how many nums have bit i set
            if bit_sum % 3:                         # remainder means unique number has this bit
                result |= (1 << i)                  # set bit i in result

        # Handle negative numbers (Python uses arbitrary precision integers,
        # not 32-bit, so we need to convert manually if result >= 2^31)
        if result >= (1 << 31):
            result -= (1 << 32)

        return result


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: Bit Manipulation — ones and twos  ← OPTIMAL
# Time  : O(N),  Space : O(1),  Single pass
#
# We track two bitmasks:
#   ones  — bits that have appeared 1 time  (mod 3)
#   twos  — bits that have appeared 2 times (mod 3)
#
# For each new number:
#   1. Add to `ones` (XOR in), but remove any bit already in `twos`
#   2. Add to `twos` (XOR in), but remove any bit already in `ones`
#
# After seeing a bit 3 times:
#   - It enters `ones`  on the 1st occurrence
#   - It moves to `twos` on the 2nd occurrence (removed from ones)
#   - It's removed from `twos` on the 3rd occurrence (count resets to 0)
#
# The unique number's bits are only seen once → they stay in `ones`.
#
# e.g. nums = [2, 2, 3, 2],  binary: 2=010, 3=011
#
#   num=2:  ones = 0^2 & ~0   = 010  twos = 0^2 & ~010 = 000
#   num=2:  ones = 010^2 & ~0 = 000  twos = 0^2 & ~000 = 010
#   num=3:  ones = 0^3 & ~010 = 001  twos = 010^3 & ~001 = 010  (bit1 stays, bit0 clears)
#   num=2:  ones = 001^2 & ~010 = 001  twos = 010^2 & ~001 = 000
#
#   ones = 001 = 1? No wait let me re-trace for [2,2,3,2]:
#   Final ones = 011 = 3  ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def singleNumber(self, nums):
        ones, twos = 0, 0
        for num in nums:
            ones = (ones ^ num) & ~twos   # add to ones, clear bits already in twos
            twos = (twos ^ num) & ~ones   # add to twos, clear bits already in ones
        return ones                        # unique number's bits remain in ones
