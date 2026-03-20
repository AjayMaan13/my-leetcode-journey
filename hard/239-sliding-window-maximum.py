# 239. Sliding Window Maximum (Hard)
# Tags: Monotonic Deque
#
# Given an array of integers nums with a sliding window of size k,
# return the max of each window position.
#
# Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 → [3,3,5,5,6,7]

# Brute Force → First Solution (Monotonic Stack with list)
class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        res = []

        stack = []
        n = len(nums)

        for i in range(k):
            cur = nums[i]
            while stack and nums[stack[-1]] < cur:
                stack.pop()
            stack.append(i)

        res.append(nums[stack[0]])

        for i in range(k, n):
            cur = nums[i]
            while stack and (nums[stack[-1]] < cur or stack[-1] < i + 1 - k):
                stack.pop()

            stack.append(i)
            if stack[0] < i + 1 - k:
                stack.pop(0)
            res.append(nums[stack[0]])

        return res


# Optimized (avoid pop(0) with left pointer)
class Solution2(object):
    def maxSlidingWindow(self, nums, k):
        res = []

        stack = []
        n = len(nums)
        left = 0

        for i in range(k):
            cur = nums[i]
            while stack and nums[stack[-1]] < cur:
                stack.pop()
            stack.append(i)

        res.append(nums[stack[0]])

        for i in range(k, n):
            cur = nums[i]
            while stack and (nums[stack[-1]] < cur or stack[-1] < i + 1 - k):
                stack.pop()

            if not stack:
                left = 0
            stack.append(i)
            if stack[left] < i + 1 - k:
                left += 1
            res.append(nums[stack[left]])

        return res


# Most Optimal — Monotonic Deque (O(n) time, O(k) space)
from collections import deque

class Solution3(object):
    def maxSlidingWindow(self, nums, k):
        res = []
        dq = deque()

        for i in range(len(nums)):
            # remove smaller elements from back
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()

            dq.append(i)

            # remove out-of-window index from front
            if dq[0] < i - k + 1:
                dq.popleft()

            # record result once first window is complete
            if i >= k - 1:
                res.append(nums[dq[0]])

        return res


# Alternate Optimal — process first window separately
class Solution4(object):
    def maxSlidingWindow(self, nums, k):
        ans = []
        dq = deque()

        # First window
        for i in range(k):
            while len(dq) > 0 and nums[dq[-1]] <= nums[i]:
                dq.pop()
            dq.append(i)

        # Remaining windows
        for i in range(k, len(nums)):
            ans.append(nums[dq[0]])

            while len(dq) > 0 and dq[0] <= i - k:
                dq.popleft()

            while len(dq) > 0 and nums[dq[-1]] <= nums[i]:
                dq.pop()
            dq.append(i)

        ans.append(nums[dq[0]])

        return ans
