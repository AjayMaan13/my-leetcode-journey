"""
930. Binary Subarrays With Sum

Given a binary array nums and integer goal, return the number of non-empty
subarrays whose elements sum to exactly goal.

Example 1: nums=[1,0,1,0,1], goal=2 -> 4
Example 2: nums=[0,0,0,0,0], goal=0 -> 15

Constraints:
- 1 <= nums.length <= 3 * 10^4
- nums[i] is either 0 or 1
- 0 <= goal <= nums.length

Key idea (prefix sum):
  If prefix[r] - prefix[l-1] == goal, then subarray [l..r] sums to goal.
  Equivalently: prefix[r] - goal == some previous prefix sum.
  Use a hashmap to count how many times each prefix sum has appeared.
"""

# ===== Brute Force =====
# Try every subarray, accumulate sum, count when it hits goal.
# Time: O(n^2) | Space: O(1)

class SolutionBrute(object):
    def numSubarraysWithSum(self, nums, goal):
        n     = len(nums)
        count = 0

        for i in range(n):
            total = 0
            for j in range(i, n):
                total += nums[j]
                if total == goal:
                    count += 1
                if total > goal:    # binary array — sum can only grow, stop early
                    break

        return count


# ===== My Solution — Prefix Sum Hashmap =====
# For each index r, we want to know how many previous indices l exist such that
# prefix[r] - prefix[l] == goal, i.e. prefix[l] == prefix[r] - goal.
# Store each prefix sum in a hashmap as we go — O(1) lookup per step.
# prefix = {0: 1} handles subarrays starting at index 0 (empty prefix has sum 0).
# Time: O(n) | Space: O(n)

class SolutionOptimal(object):
    def numSubarraysWithSum(self, nums, goal):
        total  = 0
        count  = 0
        prefix = {0: 1}   # important: accounts for subarrays starting from index 0

        for r in range(len(nums)):
            total += nums[r]

            count += prefix.get(total - goal, 0)   # how many prior prefixes match

            prefix[total] = 1 + prefix.get(total, 0)

        return count


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    optimal = SolutionOptimal()

    test_cases = [
        ([1, 0, 1, 0, 1], 2, 4),
        ([0, 0, 0, 0, 0], 0, 15),
        ([1, 0, 1],       1, 4),
        ([1, 1, 1],       2, 2),
        ([0, 0, 1],       0, 3),
    ]

    for nums, goal, expected in test_cases:
        r1 = brute.numSubarraysWithSum(nums[:], goal)
        r2 = optimal.numSubarraysWithSum(nums[:], goal)
        status = "PASS" if r1 == expected and r2 == expected else "FAIL"
        print(f"{status} nums={nums} goal={goal} -> brute={r1}, optimal={r2} (expected {expected})")
