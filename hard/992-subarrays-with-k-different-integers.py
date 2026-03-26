"""
992. Subarrays with K Different Integers

Return the number of subarrays with EXACTLY k distinct integers.

Example 1: nums=[1,2,1,2,3], k=2 -> 7
Example 2: nums=[1,2,1,3,4], k=3 -> 3

Constraints:
- 1 <= nums.length <= 2 * 10^4
- 1 <= nums[i] <= nums.length
- 1 <= k <= nums.length

Key insight (for optimal):
  exactly(k) = atMost(k) - atMost(k-1)
  Sliding window handles atMost easily — exactly is hard directly.
"""

# ===== Brute Force =====
# Try every subarray, count distinct — increment result when count == k.
# Time: O(n^2) | Space: O(k)

class SolutionBrute(object):
    def subarraysWithKDistinct(self, nums, k):
        n     = len(nums)
        count = 0

        for i in range(n):
            freq = {}
            for j in range(i, n):
                freq[nums[j]] = freq.get(nums[j], 0) + 1

                if len(freq) == k:
                    count += 1
                elif len(freq) > k:     # can only grow — stop early
                    break

        return count


# ===== My First Approach (❌ WRONG — Double Counts) =====
# Idea: when window has exactly k distinct, count extensions to the right.
# WHY IT FAILS: those same extended subarrays get counted AGAIN
# when r advances to those positions later in the outer loop.
# e.g. [1,2,1,2,3] k=2: [1,2,1] gets counted at r=1 (as extension)
# AND again at r=2 (as the main window). Double-counted.

class SolutionWrong(object):
    def subarraysWithKDistinct(self, nums, k):
        freq  = {}
        l     = 0
        count = 0

        for r in range(len(nums)):
            freq[nums[r]] = 1 + freq.get(nums[r], 0)

            while len(freq) > k:
                freq[nums[l]] -= 1
                if freq[nums[l]] == 0:
                    del freq[nums[l]]
                l += 1

            if len(freq) == k:
                count += 1                              # ❌ counts current window
                new = r + 1
                while new < len(nums) and nums[new] in freq:
                    count += 1                          # ❌ counts extensions — but these
                    new += 1                            #    will be recounted when r reaches them


        return count


# ===== My Second Approach (✅ Correct, O(n^2) worst case) =====
# Fix: at each r where exactly k distinct, count ALL valid left boundaries
# by walking temp_l rightward until the window drops below k distinct.
# Avoids double-counting but copies freq map each time → O(n) inner loop.

class SolutionO2(object):
    def subarraysWithKDistinct(self, nums, k):
        freq  = {}
        l     = 0
        count = 0

        for r in range(len(nums)):
            freq[nums[r]] = 1 + freq.get(nums[r], 0)

            while len(freq) > k:
                freq[nums[l]] -= 1
                if freq[nums[l]] == 0:
                    del freq[nums[l]]
                l += 1

            if len(freq) == k:
                temp_l    = l
                temp_freq = freq.copy()                 # snapshot current window

                # slide temp_l right while window stays exactly k distinct
                while len(temp_freq) == k:
                    count += 1                          # each temp_l is a valid left boundary
                    temp_freq[nums[temp_l]] -= 1
                    if temp_freq[nums[temp_l]] == 0:
                        del temp_freq[nums[temp_l]]
                    temp_l += 1

        return count


# ===== Optimal — atMost(k) - atMost(k-1) Trick =====
#
# Directly counting "exactly k" with a window is hard because shrinking l
# can overshoot (drop below k) and you lose valid left boundaries.
#
# Key insight:
#   exactly(k) = atMost(k) - atMost(k-1)
#
# atMost(k): for each r, the window [l..r] is the LARGEST valid window
# ending at r with <= k distinct. Every subarray [l'..r] where l <= l' <= r
# is also valid. So there are (r - l + 1) subarrays ending at r.
# Summing this over all r gives total subarrays with AT MOST k distinct.
#
# Subtracting atMost(k-1) cancels out all windows with < k distinct,
# leaving exactly k.
# Time: O(n) | Space: O(k)

class SolutionOptimal(object):
    def subarraysWithKDistinct(self, nums, k):

        def at_most(nums, k):
            freq     = {}
            l        = 0
            distinct = 0
            count    = 0

            for r in range(len(nums)):
                freq[nums[r]] = 1 + freq.get(nums[r], 0)
                if freq[nums[r]] == 1:      # new distinct element entered window
                    distinct += 1

                while distinct > k:         # too many distinct — shrink from left
                    freq[nums[l]] -= 1
                    if freq[nums[l]] == 0:
                        distinct -= 1       # distinct element left window entirely
                    l += 1

                count += (r - l + 1)        # all subarrays [l..r], [l+1..r], ..., [r..r]

            return count

        return at_most(nums, k) - at_most(nums, k - 1)


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    sol_o2  = SolutionO2()
    optimal = SolutionOptimal()

    test_cases = [
        ([1, 2, 1, 2, 3], 2, 7),
        ([1, 2, 1, 3, 4], 3, 3),
        ([1],             1, 1),
        ([1, 2, 3, 4, 5], 1, 5),
        ([1, 1, 1, 1],    1, 10),
    ]

    for nums, k, expected in test_cases:
        r1 = brute.subarraysWithKDistinct(nums[:], k)
        r2 = sol_o2.subarraysWithKDistinct(nums[:], k)
        r3 = optimal.subarraysWithKDistinct(nums[:], k)
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected else "FAIL"
        print(f"{status} nums={nums} k={k} -> brute={r1}, O(n2)={r2}, optimal={r3} (expected {expected})")
