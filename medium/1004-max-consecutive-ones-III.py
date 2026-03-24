"""
1004. Max Consecutive Ones III

Given a binary array nums and integer k, return the length of the longest
subarray of 1s you can get by flipping at most k zeros.

Example 1: nums=[1,1,1,0,0,0,1,1,1,1,0], k=2 -> 6
Example 2: nums=[0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k=3 -> 10

Constraints:
- 1 <= nums.length <= 10^5
- nums[i] is 0 or 1
- 0 <= k <= nums.length

Key idea (sliding window):
  Maintain a window [l, r] that contains at most k zeros.
  Window is valid as long as zeroCount <= k.
  Track the maximum valid window length seen.
"""

# ===== Brute Force =====
# Try every subarray, count zeros — keep the longest with zeros <= k.
# Time: O(n^2) | Space: O(1)

class SolutionBrute(object):
    def longestOnes(self, nums, k):
        n    = len(nums)
        maxL = 0

        for i in range(n):
            zeros = 0
            for j in range(i, n):
                if nums[j] == 0:
                    zeros += 1
                if zeros > k:       # too many zeros — window invalid
                    break
                maxL = max(maxL, j - i + 1)

        return maxL


# ===== My Solution — Sliding Window (shrink while invalid) =====
# Expand r each step. When zeroCount exceeds k, shrink l until valid again.
# Inner while loop handles cases where multiple zeros need to be passed.
# Time: O(n) | Space: O(1)

class SolutionMine(object):
    def longestOnes(self, nums, k):
        if not nums:
            return 0

        l         = 0
        maxL      = 0
        zeroCount = 0

        for r in range(len(nums)):
            if nums[r] == 0:
                zeroCount += 1
                if zeroCount > k:
                    while zeroCount > k:        # shrink from left until window is valid
                        if nums[l] == 0:
                            zeroCount -= 1
                        l += 1
            maxL = max(maxL, r - l + 1)

        return maxL


# ===== Optimized — Sliding Window (fixed-size slide) =====
# Key insight: we only care about the MAXIMUM window ever seen.
# So when the window becomes invalid, instead of shrinking it,
# just SLIDE it forward by 1 — this preserves the best size found so far.
# l moves forward exactly once per r step → cleaner, no inner loop.
# Time: O(n) | Space: O(1)

class SolutionOptimal(object):
    def longestOnes(self, nums, k):
        l = 0

        for r in range(len(nums)):
            if nums[r] == 0:
                k -= 1              # used a flip for this zero

            if k < 0:               # window has too many zeros — slide forward
                if nums[l] == 0:
                    k += 1          # reclaim the flip as left edge leaves window
                l += 1

        return r - l + 1            # window never shrinks, so final size = max size


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    mine    = SolutionMine()
    optimal = SolutionOptimal()

    test_cases = [
        ([1,1,1,0,0,0,1,1,1,1,0],              2, 6),
        ([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3, 10),
        ([1,1,1,1],                             0, 4),
        ([0,0,0,0],                             0, 0),
        ([0,0,0,0],                             4, 4),
        ([1],                                   1, 1),
    ]

    for nums, k, expected in test_cases:
        r1 = brute.longestOnes(nums[:], k)
        r2 = mine.longestOnes(nums[:], k)
        r3 = optimal.longestOnes(nums[:], k)
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected else "FAIL"
        print(f"{status} k={k} nums={nums} -> brute={r1}, mine={r2}, optimal={r3} (expected {expected})")
