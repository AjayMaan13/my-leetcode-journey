"""
1248. Count Number of Nice Subarrays

A subarray is "nice" if it contains exactly k odd numbers.
Return the count of nice subarrays.

Example 1: nums=[1,1,2,1,1], k=3 -> 2  ([1,1,2,1] and [1,2,1,1])
Example 2: nums=[2,4,6],     k=1 -> 0
Example 3: nums=[2,2,2,1,2,2,1,2,2,2], k=2 -> 16

Constraints:
- 1 <= nums.length <= 50000
- 1 <= nums[i] <= 10^5
- 1 <= k <= nums.length

Key idea:
  Same pattern as "Subarray Sum Equals K" (LC 930).
  Replace each number with 1 (odd) or 0 (even) → count subarrays summing to k.
  Use prefix sum hashmap: for each r, count how many l's give exactly k odds.
"""

# ===== Brute Force =====
# Try every subarray, count odds — increment result when count == k.
# Time: O(n^2) | Space: O(1)

class SolutionBrute(object):
    def numberOfSubarrays(self, nums, k):
        n     = len(nums)
        count = 0

        for i in range(n):
            odds = 0
            for j in range(i, n):
                if nums[j] % 2 != 0:
                    odds += 1
                if odds == k:
                    count += 1
                elif odds > k:      # can only grow — stop early
                    break

        return count


# ===== My Solution — Prefix Sum Hashmap =====
# Track a running count of odd numbers seen so far (freq).
# For each r: how many prior indices had freq = (current_freq - k)?
# Those indices form valid left boundaries giving exactly k odds.
# prefix = {0: 1} handles subarrays starting at index 0.
# Total Sum - Preferred Sum
# Time: O(n) | Space: O(n)

class SolutionOptimal(object):
    def numberOfSubarrays(self, nums, k):
        if not nums:
            return 0

        prefix = {0: 1}   # odd_count -> how many times seen
        freq   = 0
        count  = 0

        for r in range(len(nums)):
            if nums[r] % 2 != 0:
                freq += 1              # odd number found — increment prefix count

            count += prefix.get(freq - k, 0)   # how many left boundaries give exactly k odds

            # Total Sum - Preferred Sum
            prefix[freq] = 1 + prefix.get(freq, 0)

        return count


# ===== atMost Sliding Window — exactly(k) = atMost(k) - atMost(k-1) =====
# Same trick as LC 930. Treat each number as 1 (odd) or 0 (even).
# atMost(k): for each r, [l..r] is the largest window with <= k odds.
#             There are (r - l + 1) subarrays ending at r with <= k odds.
# Subtracting atMost(k-1) cancels windows with < k odds, leaving exactly k.
# Time: O(n) | Space: O(1) — no hashmap needed

class SolutionAtMost(object):
    def numberOfSubarrays(self, nums, k):

        def at_most(nums, k):
            if k < 0:
                return 0
            l     = 0
            odds  = 0
            count = 0
            for r in range(len(nums)):
                if nums[r] % 2 != 0:
                    odds += 1               # odd number enters window
                while odds > k:             # too many odds — shrink from left
                    if nums[l] % 2 != 0:
                        odds -= 1           # odd number leaves window
                    l += 1
                count += r - l + 1          # all subarrays ending at r with <= k odds
            return count

        return at_most(nums, k) - at_most(nums, k - 1)


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    optimal = SolutionOptimal()
    at_most = SolutionAtMost()

    test_cases = [
        ([1, 1, 2, 1, 1],          3, 2),
        ([2, 4, 6],                1, 0),
        ([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2, 16),
        ([1],                      1, 1),
        ([2, 2, 2],                1, 0),
        ([1, 1, 1],                2, 2),
    ]

    for nums, k, expected in test_cases:
        r1 = brute.numberOfSubarrays(nums[:], k)
        r2 = optimal.numberOfSubarrays(nums[:], k)
        r3 = at_most.numberOfSubarrays(nums[:], k)
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected else "FAIL"
        print(f"{status} nums={nums} k={k} -> brute={r1}, prefix={r2}, at_most={r3} (expected {expected})")
