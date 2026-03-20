# 239. Sliding Window Maximum (Hard)
# Tags: Monotonic Deque
#
# Given an array nums and window size k, return the max of each window as it slides right.
# Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 → [3,3,5,5,6,7]


# ─────────────────────────────────────────────
# BRUTE FORCE — O(n*k) time, O(1) space
# ─────────────────────────────────────────────
# For each window of size k, scan all k elements to find the max.
# Simple but slow — repeats work for overlapping windows.

class Solution(object):
    def maxSlidingWindow(self, nums, k):
        res = []
        n = len(nums)

        for i in range(n - k + 1):          # n-k+1 windows total
            window_max = max(nums[i:i + k]) # scan k elements each time → O(k)
            res.append(window_max)

        return res


# ─────────────────────────────────────────────
# FIRST SOLUTION — Monotonic Stack (list) — O(n) time, O(n) space
# ─────────────────────────────────────────────
# Key idea: maintain a stack of indices in DECREASING order of their values.
# The front of the stack is always the index of the current window's max.
#
# When adding index i:
#   - pop from the back any index whose value < nums[i]  (they can never be max)
#   - pop from the back any index outside the window     (stale)
# When reading max:
#   - check if front index fell out of window → pop(0)   (O(k) worst case)
#
# Problem: pop(0) on a list is O(n). Fixed in Solution2 with a left pointer.

class Solution2(object):
    def maxSlidingWindow(self, nums, k):
        res = []
        stack = []  # stores indices, values are decreasing front→back
        n = len(nums)

        # Build first window
        for i in range(k):
            # remove indices whose values are smaller than current (useless candidates)
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            stack.append(i)

        res.append(nums[stack[0]])  # front of stack = max of first window

        for i in range(k, n):
            # remove from back: stale indices AND indices with smaller values
            while stack and (nums[stack[-1]] < nums[i] or stack[-1] < i + 1 - k):
                stack.pop()

            stack.append(i)

            # if front index fell out of the window, remove it (O(k) worst case)
            if stack[0] < i + 1 - k:
                stack.pop(0)

            res.append(nums[stack[0]])

        return res


# ─────────────────────────────────────────────
# OPTIMIZED — Left pointer instead of pop(0) — O(n) time, O(n) space
# ─────────────────────────────────────────────
# Same as above but instead of pop(0) (which shifts the whole list),
# track a `left` pointer to the valid front of the stack.
# The max is always at stack[left].

class Solution3(object):
    def maxSlidingWindow(self, nums, k):
        res = []
        stack = []
        n = len(nums)
        left = 0  # pointer to the front of the valid portion of stack

        # Build first window
        for i in range(k):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            stack.append(i)

        res.append(nums[stack[left]])

        for i in range(k, n):
            while stack and (nums[stack[-1]] < nums[i] or stack[-1] < i + 1 - k):
                stack.pop()

            if not stack:
                left = 0  # reset if stack was fully cleared
            stack.append(i)

            # advance left pointer if the front index is outside the window
            if stack[left] < i + 1 - k:
                left += 1

            res.append(nums[stack[left]])

        return res


# ─────────────────────────────────────────────
# MOST OPTIMAL — Monotonic Deque — O(n) time, O(k) space
# ─────────────────────────────────────────────
# Use a deque (double-ended queue) to get O(1) pops from both ends.
# Deque stores indices in decreasing order of values (front = current max).
#
# For each index i:
#   1. Pop from BACK  — remove indices with values ≤ nums[i] (they're now dominated)
#   2. Append i to BACK
#   3. Pop from FRONT — remove index if it's outside the current window [i-k+1 .. i]
#   4. Record result  — deque front is the max, but only after the first window fills

from collections import deque

class Solution4(object):
    def maxSlidingWindow(self, nums, k):
        res = []
        dq = deque()  # stores indices; nums[dq[0]] is always the window max

        for i in range(len(nums)):
            # step 1: new element dominates smaller ones → pop from back
            while dq and nums[dq[-1]] < nums[i]:
                dq.pop()

            # step 2: add current index
            dq.append(i)

            # step 3: front index outside window → evict it
            if dq[0] < i - k + 1:
                dq.popleft()

            # step 4: first full window reached → record max
            if i >= k - 1:
                res.append(nums[dq[0]])

        return res


# ─────────────────────────────────────────────
# ALTERNATE OPTIMAL — first window separate — O(n) time, O(k) space
# ─────────────────────────────────────────────
# Same deque approach but processes the first window in its own loop,
# then handles remaining windows. Slightly cleaner separation of concerns.

class Solution5(object):
    def maxSlidingWindow(self, nums, k):
        ans = []
        dq = deque()

        # Fill the first window (no result yet)
        for i in range(k):
            while dq and nums[dq[-1]] <= nums[i]:
                dq.pop()
            dq.append(i)

        # Slide remaining windows
        for i in range(k, len(nums)):
            ans.append(nums[dq[0]])             # record max BEFORE sliding

            while dq and dq[0] <= i - k:        # evict out-of-window front
                dq.popleft()

            while dq and nums[dq[-1]] <= nums[i]: # remove dominated back elements
                dq.pop()
            dq.append(i)

        ans.append(nums[dq[0]])                  # last window max

        return ans
