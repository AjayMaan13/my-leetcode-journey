"""
Count All Subsequences with Sum K  |  TUF Problem

Problem Statement:
    Given an array nums and an integer k, return the number of non-empty
    subsequences of nums such that the sum of all elements equals k.

Examples:
    nums = [4, 9, 2, 5, 1],    k = 10  →  2   ([9,1], [4,5,1])
    nums = [4, 2, 10, 5, 1, 3], k = 5  →  3   ([4,1], [2,3], [5])
    nums = [1, 2, 3, 4, 5],    k = 5   →  3   ([5], [1,4], [2,3])

Key Insight:
    At every index we make a binary decision: INCLUDE or EXCLUDE the element.
    This is the same "power set" recursion from the previous problem —
    the only addition is a running sum and a target check at the leaf/base case.

    Recursion tree for [1,2,3], k=3:
                            func(0, 3)
                        /              \\
              func(1, 2)            func(1, 3)       ← exclude 1
             /        \\            /         \\
        func(2,0)  func(2,2)  func(2,1)   func(2,3)  ← exclude 2
         sum=0 ✓    /    \\     /    \\      /     \\
                f(3,-1) f(3,2) f(3,-2) f(3,1) f(3,0)✓ f(3,3)
                  ✗      ✗      ✗       ✗      ✓       ✗
    Count = 2  ([1,2] and [3])  wait k=3 so [1,2] sums to 3 ✓, [3] sums to 3 ✓
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: PURE RECURSION
# Time  : O(2^n)  — every element has 2 choices: include or exclude
# Space : O(n)    — recursion depth = n
#
# At each step reduce the remaining target by nums[ind] (include)
# or keep it unchanged (exclude). Return 1 when target hits exactly 0.
#
# NOTE: checking `sum == 0` BEFORE `ind == len(nums)` is important —
# it catches valid subsequences even when we haven't consumed all elements.
# e.g. nums=[1,2,3], k=1: as soon as we include 1, sum becomes 0 → count it
#      immediately without waiting to reach the end.
# ─────────────────────────────────────────────────────────────────────────────
class Solution1:
    def func(self, ind: int, remaining: int, nums: list) -> int:
        # Found a valid subsequence — remaining sum is exactly 0
        if remaining == 0:
            return 1

        # Overshot (sum went negative) OR exhausted array without hitting 0
        if remaining < 0 or ind == len(nums):
            return 0

        # Include nums[ind]: subtract from remaining target
        include = self.func(ind + 1, remaining - nums[ind], nums)

        # Exclude nums[ind]: remaining target unchanged
        exclude = self.func(ind + 1, remaining, nums)

        return include + exclude

    def countSubsequenceWithTargetSum(self, nums: list, target: int) -> int:
        return self.func(0, target, nums)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: RECURSION — track index as stopping condition (index-first style)
# Time  : O(2^n)
# Space : O(n)
#
# Same idea but check index FIRST (end of array), then check sum at the leaf.
# This is the more common backtracking pattern you've seen in previous problems
# (power set, generate parentheses etc.) — process all n positions, then
# evaluate at the base case.
#
# Difference from Approach 1:
#   Approach 1 exits EARLY when sum hits 0 (before processing remaining elements)
#   Approach 2 always goes to depth n before checking — slightly more calls,
#   but the logic is more consistent with other backtracking problems.
# ─────────────────────────────────────────────────────────────────────────────
class Solution2:
    def countSubsequenceWithTargetSum(self, nums: list, target: int) -> int:
        result = [0]   # use list so inner function can mutate it

        def helper(ind: int, curr_sum: int) -> None:
            # Base case: processed all elements
            if ind == len(nums):
                if curr_sum == target:   # check if current subset sums to k
                    result[0] += 1
                return

            # Include nums[ind]
            helper(ind + 1, curr_sum + nums[ind])

            # Exclude nums[ind]
            helper(ind + 1, curr_sum)

        helper(0, 0)
        return result[0]


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: MEMOIZATION (Top-Down DP)
# Time  : O(n * k)  — each (ind, remaining) pair computed at most once
# Space : O(n * k)  — memo table size
#
# Approach 1 recomputes the same (ind, remaining) subproblems multiple times.
# Cache them using a dictionary to avoid redundant work.
#
# When does memoization help here?
#   If the array has duplicate values, different paths through the recursion
#   tree can reach the same (ind, remaining) state. Memoization collapses
#   these repeated computations.
#
# Example: nums=[1,1,1,1], k=2 — many paths reach (ind=2, remaining=1)
#   Without memo: O(2^4) = 16 calls
#   With memo:    O(n*k) states = much fewer for large n with repeated values
# ─────────────────────────────────────────────────────────────────────────────
class Solution3:
    def countSubsequenceWithTargetSum(self, nums: list, target: int) -> int:
        memo = {}   # (ind, remaining) → count

        def func(ind: int, remaining: int) -> int:
            if remaining == 0:
                return 1
            if remaining < 0 or ind == len(nums):
                return 0

            if (ind, remaining) in memo:
                return memo[(ind, remaining)]

            include = func(ind + 1, remaining - nums[ind])
            exclude = func(ind + 1, remaining)

            memo[(ind, remaining)] = include + exclude
            return memo[(ind, remaining)]

        return func(0, target)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 4: BOTTOM-UP DP (Tabulation)
# Time  : O(n * k)
# Space : O(n * k)  — DP table, or O(k) with space optimization
#
# Build a 2D DP table where:
#   dp[i][j] = number of subsequences using the first i elements with sum = j
#
# Transition:
#   dp[i][j] = dp[i-1][j]               ← exclude nums[i-1]
#            + dp[i-1][j - nums[i-1]]   ← include nums[i-1] (if j >= nums[i-1])
#
# Base case:
#   dp[0][0] = 1  (empty subsequence has sum 0 — 1 way to achieve sum 0 with 0 elements)
#   dp[0][j] = 0  for j > 0
#
# Note: this counts the empty subsequence if target=0. The problem asks for
# NON-EMPTY subsequences. We handle this by initializing dp[0][0]=1 but
# the recursion already handles it (sum==0 only reached by non-empty paths
# because we start with target > 0 in the test cases).
# ─────────────────────────────────────────────────────────────────────────────
class Solution4:
    def countSubsequenceWithTargetSum(self, nums: list, target: int) -> int:
        n = len(nums)

        # dp[i][j] = # of subsequences from first i elements that sum to j
        dp = [[0] * (target + 1) for _ in range(n + 1)]
        dp[0][0] = 1    # base: empty set sums to 0 in exactly 1 way

        for i in range(1, n + 1):
            for j in range(target + 1):
                # Always include the "exclude" case
                dp[i][j] = dp[i - 1][j]

                # Add "include" case if current element fits
                if j >= nums[i - 1]:
                    dp[i][j] += dp[i - 1][j - nums[i - 1]]

        return dp[n][target]

