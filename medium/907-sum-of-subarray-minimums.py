"""
907. Sum of Subarray Minimums

For every contiguous subarray of arr, find its minimum, then return
the sum of all those minimums (mod 10^9 + 7).

Example:
  arr = [3,1,2,4]
  Subarrays + minimums: [3]->3, [1]->1, [2]->2, [4]->4,
                        [3,1]->1, [1,2]->1, [2,4]->2,
                        [3,1,2]->1, [1,2,4]->1, [3,1,2,4]->1
  Sum = 17

Constraints:
- 1 <= arr.length <= 3 * 10^4
- 1 <= arr[i] <= 3 * 10^4

Key idea (for the optimal solution):
  Instead of summing over subarrays, sum over each ELEMENT.
  For each arr[i], count how many subarrays have arr[i] as their minimum.
  Then: answer = sum(arr[i] * count_i) for all i.
"""

# ===== My Original Solution (TLE — Recursive Brute Force) =====
# Generates every subarray via recursion, computes min(arr[start:end+1]) each time.
# Time: O(n^3) — O(n^2) subarrays, O(n) per min call | Space: O(n) call stack

class SolutionBrute(object):
    def sumSubarrayMins(self, arr):
        if not arr:
            return 0

        def helper(start, end):
            if start == len(arr):
                return 0
            if end == len(arr):
                return helper(start + 1, start + 1)  # move to next starting point

            current = min(arr[start:end + 1])         # min of current subarray
            return current + helper(start, end + 1)   # extend subarray rightward

        return helper(0, 0)


# ===== Solution 2 (TLE — O(n^2) Contribution, no stack) =====
# For each index i, expand left and right to count subarrays where arr[i] is min.
# left  = how many consecutive elements to the left are >= arr[i] (including arr[i])
# right = how many consecutive elements to the right are >  arr[i] (including arr[i])
# contribution of arr[i] = arr[i] * left * right
# Uses >= left / > right to avoid double-counting duplicate minimums.
# Time: O(n^2) worst case | Space: O(1)

class SolutionO2(object):
    def sumSubarrayMins(self, arr):
        MOD = 10**9 + 7
        n   = len(arr)
        ans = 0

        for i in range(n):
            left = 1
            j = i - 1
            while j >= 0 and arr[j] >= arr[i]:  # go left while elements are >= arr[i]
                left += 1
                j -= 1

            right = 1
            j = i + 1
            while j < n and arr[j] > arr[i]:    # go right while elements are strictly > arr[i]
                right += 1
                j += 1

            ans = (ans + arr[i] * left * right) % MOD

        return ans

# ===== Optimal Solution (Monotonic Stack — O(n)) =====
#
# Same contribution idea as Solution 2 but we precompute left[] and right[]
# for ALL elements in O(n) using a monotonic stack instead of O(n) per element.
#
# For each index i we need:
#   left[i]  = i - (index of previous element strictly smaller than arr[i])
#            = number of choices for the LEFT boundary of subarrays where arr[i] is min
#   right[i] = (index of next element <= arr[i]) - i
#            = number of choices for the RIGHT boundary
#
# Why asymmetric comparisons (< vs <=)?
#   To handle DUPLICATES without double-counting.
#   If arr = [2, 2], both elements can't both be the min of the full subarray [2,2].
#   Left uses strict '<' (pop on >=) → left element "wins" ties.
#   Right uses '<=' (pop on >) → right element does NOT claim tie subarrays.
#   This ensures each subarray is counted by exactly one index.
#
# Contribution formula: arr[i] * left[i] * right[i]
#   left[i] * right[i] = total subarrays where arr[i] is the minimum.

# Precompute left[] and right[] for ALL elements in two separate passes.
# left[i]  = how far left arr[i] can extend as the minimum (previous smaller is the wall)
# right[i] = how far right arr[i] can extend as the minimum (next smaller-or-equal is the wall)
# Asymmetric comparisons handle duplicates — left uses >, right uses >= on pop,
# so ties are always "won" by the LEFT occurrence (no double-counting).
# Time: O(n) | Space: O(n)

class SolutionOptimal(object):
    def sumSubarrayMins(self, arr):
        # i = arr[i] * left_extend * right_extend
        # left index is values smaller than arr[i] i.e previous smaller
        # right index is values equal or greater than arr[i] next greater
        MOD = 10**9 + 7
        left = [0] * len(arr)
        right = [0] * len(arr)
        res = 0

        stack = []
        for i in range(len(arr)):
            curr = arr[i]

            # we want to store the last smallest value cause it shows us the
            # breaking point of where the bigger values to left extend to
            while stack and arr[stack[-1]] > curr:
                stack.pop()

            # distance from previous smaller to i (inclusive) = left extension count
            left[i] = i - stack[-1] if stack else i + 1
            stack.append(i)

        stack = []
        for i in range(len(arr) - 1, -1, -1):
            curr = arr[i]

            # pop bigger values so that we know how much it extend to the right
            while stack and arr[stack[-1]] >= curr:
                stack.pop()

            # distance from i to next smaller-or-equal (inclusive) = right extension count
            right[i] = stack[-1] - i if stack else len(arr) - i
            stack.append(i)

        for i in range(len(arr)):
            res += arr[i] * left[i] * right[i]

        return res % MOD


# ===== Optimal Solution 2: Single-Pass Monotonic Stack (On-Pop Contribution) =====
# Instead of two separate passes, compute each element's contribution the moment it's popped.
# When index `popped` is popped, arr[popped] is confirmed as minimum for a range:
#   left  boundary = stack[-1] after pop (nearest smaller to left)
#   right boundary = i (current index that triggered the pop, first smaller to right)
# Sentinel cur=0 at i=len(arr) flushes all remaining stack elements cleanly.
# Time: O(n) | Space: O(n)

class SolutionSinglePass(object):
    def sumSubarrayMins(self, arr):
        MOD = 10**9 + 7
        res = 0

        stack = []
        for i in range(len(arr) + 1):
            cur = arr[i] if i < len(arr) else 0  # sentinel 0 forces full flush at end

            while stack and arr[stack[-1]] > cur:
                popped = stack.pop()

                # popped - last_smallest contain all the values that are bigger than popped in between, so we don't need to add 1
                left = popped - stack[-1] if stack else popped + 1

                # i is the next smallest, i.e breaking point and diff = all values bigger than popped
                right = i - popped
                res += arr[popped] * left * right

            stack.append(i)

        return res % MOD


# ===== Test Cases =====
if __name__ == "__main__":
    brute       = SolutionBrute()
    sol_o2      = SolutionO2()
    optimal     = SolutionOptimal()
    single_pass = SolutionSinglePass()

    test_cases = [
        ([3, 1, 2, 4],        17),
        ([11, 81, 94, 43, 3], 444),
        ([1],                  1),
        ([3, 3],               9),   # duplicate: [3]->3, [3]->3, [3,3]->3 = 9
        ([1, 2, 3],           10),
    ]

    for arr, expected in test_cases:
        r1 = brute.sumSubarrayMins(arr[:])
        r2 = sol_o2.sumSubarrayMins(arr[:])
        r3 = optimal.sumSubarrayMins(arr[:])
        r4 = single_pass.sumSubarrayMins(arr[:])
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected and r4 == expected else "FAIL"
        print(f"{status} arr={arr} -> brute={r1}, O(n2)={r2}, two-pass={r3}, single-pass={r4} (expected {expected})")
