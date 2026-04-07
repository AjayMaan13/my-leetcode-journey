# 55. Jump Game
# https://leetcode.com/problems/jump-game/
#
# You are given an integer array nums. You are initially positioned at index 0,
# and each element represents your maximum jump length at that position.
# Return true if you can reach the last index, or false otherwise.
#
# Example 1:
#   Input: nums = [2,3,1,1,4]
#   Output: true
#   Explanation: Jump 1 step from index 0 to index 1, then 3 steps to the last index.
#
# Example 2:
#   Input: nums = [3,2,1,0,4]
#   Output: false
#   Explanation: You always land on index 3 (max jump = 0), so index 4 is unreachable.
#
# Constraints:
#   1 <= nums.length <= 10^4
#   0 <= nums[i] <= 10^5


# DP (Reachability Array) - O(n^2) time, O(n) space
# can[i] = True if index i is reachable from index 0.
# For each reachable index i, mark all indices in range [i+1, i+nums[i]] as reachable.
# At the end, if any index is still False, we can't reach it — return False.
class SolutionDP:
    def canJump(self, nums):
        if len(nums) < 2:
            return True

        can = [False] * len(nums)
        can[0] = nums[0] > 0  # index 0 is only "jumpable" if nums[0] > 0

        for i in range(len(nums) - 1):
            if nums[i] > 0:
                # mark every index reachable from i as True
                end = min(i + nums[i] + 1, len(nums))
                for j in range(i + 1, end):
                    can[j] = True

        return all(can)  # every index must be reachable


# Greedy (Max Reach) - O(n) time, O(1) space
# Track max_reach: the farthest index we can reach so far.
# At each index i, if i > max_reach we're stuck — can't get here, return False.
# Otherwise update max_reach with the farthest we can jump from i.
# If max_reach ever covers the last index, return True immediately.
class Solution:
    def canJump(self, nums):
        max_reach = 0  # farthest index reachable from any visited index

        for i in range(len(nums)):
            if i > max_reach:
                return False           # index i is a gap — unreachable

            max_reach = max(max_reach, i + nums[i])  # update farthest reach

            if max_reach >= len(nums) - 1:
                return True            # last index is within reach

        return True


nums = [2, 3, 1, 1, 4]
sol = Solution()
print(sol.canJump(nums))  # True

nums = [3, 2, 1, 0, 4]
print(sol.canJump(nums))  # False
