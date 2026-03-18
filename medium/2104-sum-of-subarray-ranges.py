"""
2104. Sum of Subarray Ranges

The range of a subarray = max(subarray) - min(subarray).
Return the sum of all subarray ranges.

Example 1: nums = [1,2,3]   -> 4
Example 2: nums = [1,3,3]   -> 4
Example 3: nums = [4,-2,-3,4,1] -> 59

Constraints:
- 1 <= nums.length <= 1000
- -10^9 <= nums[i] <= 10^9

Key insight (for optimal):
  sum of (max - min) = sum of all subarray maxes - sum of all subarray mins
  Each half is exactly the "907. Sum of Subarray Minimums" pattern.
"""

# ===== Solution 1: Pure Brute Force =====
# For every subarray, slice it and call max/min directly.
# Time: O(n^3) — O(n^2) subarrays, O(n) each for max/min | Space: O(n)

class SolutionBrute(object):
    def subArrayRanges(self, nums):
        n   = len(nums)
        ans = 0

        for i in range(n):
            for j in range(i, n):
                sub  = nums[i:j + 1]
                ans += max(sub) - min(sub)   # O(n) per subarray

        return ans


# ===== Solution 2: Better Brute (running min/max) =====
# Avoid re-slicing — maintain cur_min and cur_max as we extend each subarray.
# Time: O(n^2) | Space: O(1)

class SolutionBetterBrute(object):
    def subArrayRanges(self, nums):
        n   = len(nums)
        ans = 0

        for i in range(n):
            cur_min = nums[i]
            cur_max = nums[i]

            for j in range(i, n):
                cur_min  = min(cur_min, nums[j])   # extend subarray: update running min
                cur_max  = max(cur_max, nums[j])   # extend subarray: update running max
                ans     += cur_max - cur_min

        return ans


# ===== Solution 3: Optimal — Monotonic Stack O(n) =====
#
# Rewrite the problem:
#   sum(max - min) = sum(all subarray maxes) - sum(all subarray mins)
#
# Each half is solved independently with a monotonic stack
# (same technique as 907. Sum of Subarray Minimums).
#
# sumSubarrayMins: monotonic INCREASING stack
#   → pop when arr[top] > cur (found right boundary for top as minimum)
#   → sentinel -inf at end forces full flush
#
# sumSubarrayMaxs: monotonic DECREASING stack
#   → pop when arr[top] < cur (found right boundary for top as maximum)
#   → sentinel +inf at end forces full flush
#
# On each pop of index `mid`:
#   left  = stack[-1] after pop  (nearest index where arr[left] is a better min/max)
#   right = i                    (current index that triggered the pop)
#   contribution = arr[mid] * (mid - left) * (right - mid)
#
# Time: O(n) | Space: O(n)

class SolutionOptimal(object):
    def subArrayRanges(self, nums):

        def sumSubarrayMins(arr):
            stack = []   # monotonic increasing (indices)
            res   = 0

            for i in range(len(arr) + 1):
                cur = arr[i] if i < len(arr) else float('-inf')  # sentinel flushes stack

                while stack and arr[stack[-1]] > cur:
                    mid   = stack.pop()
                    left  = stack[-1] if stack else -1   # nearest smaller to the left
                    right = i                            # first smaller to the right
                    res  += arr[mid] * (mid - left) * (right - mid)

                stack.append(i)

            return res

        def sumSubarrayMaxs(arr):
            stack = []   # monotonic decreasing (indices)
            res   = 0

            for i in range(len(arr) + 1):
                cur = arr[i] if i < len(arr) else float('inf')   # sentinel flushes stack

                while stack and arr[stack[-1]] < cur:            # flip: pop when smaller found
                    mid   = stack.pop()
                    left  = stack[-1] if stack else -1   # nearest larger to the left
                    right = i                            # first larger to the right
                    res  += arr[mid] * (mid - left) * (right - mid)

                stack.append(i)

            return res

        return sumSubarrayMaxs(nums) - sumSubarrayMins(nums)


# ===== Test Cases =====
if __name__ == "__main__":
    brute        = SolutionBrute()
    better_brute = SolutionBetterBrute()
    optimal      = SolutionOptimal()

    test_cases = [
        ([1, 2, 3],          4),
        ([1, 3, 3],          4),
        ([4, -2, -3, 4, 1], 59),
        ([1],                0),
        ([3, 3],             0),
    ]

    for nums, expected in test_cases:
        r1 = brute.subArrayRanges(nums[:])
        r2 = better_brute.subArrayRanges(nums[:])
        r3 = optimal.subArrayRanges(nums[:])
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected else "FAIL"
        print(f"{status} nums={nums} -> brute={r1}, better={r2}, optimal={r3} (expected {expected})")
