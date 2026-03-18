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
#
# Time: O(n) | Space: O(n)

class SolutionOptimal(object):
    def sumSubarrayMins(self, arr):
        MOD = 10**9 + 7
        n   = len(arr)

        left  = [0] * n   # left[i]  = distance to previous strictly smaller element
        right = [0] * n   # right[i] = distance to next smaller-or-equal element

        # --- Pass 1: Previous Smaller (strictly <) ---
        # Pop stack while top element is >= arr[i] (not a valid left boundary).
        # Stack holds indices of elements in increasing order.
        stack = []
        for i in range(n):
            while stack and arr[stack[-1]] >= arr[i]:
                stack.pop()                          # remove elements that are >= arr[i]

            prev    = stack[-1] if stack else -1     # nearest index with arr[prev] < arr[i]
            left[i] = i - prev                       # elements from prev+1 to i (inclusive)
            stack.append(i)

        # --- Pass 2: Next Smaller or Equal (<=) ---
        # Pop stack while top element is > arr[i] (arr[i] would be a better/equal min).
        # Iterate right-to-left so stack stays in order.
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()                          # remove elements strictly greater than arr[i]

            nxt      = stack[-1] if stack else n     # nearest index with arr[nxt] <= arr[i]
            right[i] = nxt - i                       # elements from i to nxt-1 (inclusive)
            stack.append(i)

        # --- Pass 3: Sum contributions ---
        ans = 0
        for i in range(n):
            ans = (ans + arr[i] * left[i] * right[i]) % MOD

        return ans


# ===== Optimal Solution 2: Single-Pass Monotonic Stack =====
# Same O(n) idea but computes contributions ON POP instead of precomputing left[]/right[].
# When we pop index `mid`, we know:
#   - arr[mid] is larger than cur (the element that caused the pop) → right boundary = i
#   - stack[-1] after popping is the previous smaller element → left boundary
# So contribution of arr[mid] = arr[mid] * (mid - left) * (right - mid)
# Appends sentinel 0 at the end (i = len(arr)) to flush remaining stack elements.
# Time: O(n) | Space: O(n)

class SolutionSinglePass(object):
    def sumSubarrayMins(self, arr):
        MOD   = 10**9 + 7
        stack = []   # monotonic increasing stack of indices
        res   = 0

        for i in range(len(arr) + 1):
            cur = arr[i] if i < len(arr) else 0   # sentinel 0 flushes remaining stack at end

            while stack and arr[stack[-1]] > cur:
                mid   = stack.pop()                # arr[mid] is the minimum for some subarrays

                left  = stack[-1] if stack else -1 # nearest index to left with arr[left] < arr[mid]
                right = i                          # current index is the first element < arr[mid] on right

                res += arr[mid] * (mid - left) * (right - mid)  # count * value

            stack.append(i)

        return res % MOD


# ===== Test Cases =====
if __name__ == "__main__":
    brute       = SolutionBrute()
    sol_o2      = SolutionO2()
    optimal     = SolutionOptimal()
    single_pass = SolutionSinglePass()

    test_cases = [
        ([3, 1, 2, 4],       17),
        ([11, 81, 94, 43, 3], 444),
        ([1],                 1),
        ([3, 3],              9),   # duplicate test: [3]->3, [3]->3, [3,3]->3 = 9
        ([1, 2, 3],          10),
    ]

    for arr, expected in test_cases:
        r1 = brute.sumSubarrayMins(arr[:])
        r2 = sol_o2.sumSubarrayMins(arr[:])
        r3 = optimal.sumSubarrayMins(arr[:])
        r4 = single_pass.sumSubarrayMins(arr[:])
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected and r4 == expected else "FAIL"
        print(f"{status} arr={arr} -> brute={r1}, O(n2)={r2}, optimal={r3}, single_pass={r4} (expected {expected})")
