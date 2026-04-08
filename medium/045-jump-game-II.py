"""
45. Jump Game II

Starting at index 0, each nums[i] tells you the max jump length from i.
Return the minimum number of jumps to reach the last index.
It's guaranteed you can always reach the end.

Example 1: nums=[2,3,1,1,4] -> 2  (0->1->4)
Example 2: nums=[2,3,0,1,4] -> 2  (0->1->4)

Constraints:
- 1 <= nums.length <= 10^4
- 0 <= nums[i] <= 1000
- Always reachable
"""

# ===== Brute Force — BFS (Level by Level) =====
# Treat each "jump" as a BFS level. Every index reachable in j jumps is one level.
# Expand all indices in the current level, collect next level, repeat.
# Time: O(n^2) — each index can be added to a level multiple times | Space: O(n)

from collections import deque

class SolutionBrute(object):
    def jump(self, nums):
        n = len(nums)
        if n < 2:
            return 0

        visited = [False] * n
        queue   = deque([0])
        visited[0] = True
        jumps   = 0

        while queue:
            jumps += 1
            for _ in range(len(queue)):     # process all indices at current jump level
                i = queue.popleft()
                for j in range(1, nums[i] + 1):
                    nxt = i + j
                    if nxt >= n - 1:
                        return jumps        # reached last index
                    if not visited[nxt]:
                        visited[nxt] = True
                        queue.append(nxt)

        return jumps


# ===== My Solution 1 — DP (O(n^2)) =====
# minJump[i] = minimum jumps to reach index i.
# For each i, update all reachable indices j in [i+1, i+nums[i]].
# Time: O(n^2) | Space: O(n)

class SolutionDP(object):
    def jump(self, nums):
        if len(nums) < 2:
            return 0

        minJump    = [float('inf')] * len(nums)
        minJump[0] = 0

        for i in range(len(nums) - 1):
            end = len(nums)
            if (i + nums[i] + 1) < len(nums):
                end = i + nums[i] + 1           # don't go past array end

            for j in range(i + 1, end):
                minJump[j] = min(minJump[j], minJump[i] + 1)

        return minJump[-1]


# ===== My Solution 2 — Greedy (O(n)) =====
# Think of it as implicit BFS — no queue needed.
# current_end = the farthest index reachable in the current jump count.
# farthest    = the farthest index reachable from any index seen so far.
# When i reaches current_end, we MUST take another jump (use farthest as next boundary).
# We never iterate past the second-to-last index — reaching it already guarantees the end.
# Time: O(n) | Space: O(1)

class SolutionGreedy(object):
    def jump(self, nums):
        jumps       = 0
        current_end = 0   # end of current jump's reachable range
        farthest    = 0   # best reach seen across all indices so far

        for i in range(len(nums) - 1):  # no need to go to last index
            farthest = max(farthest, i + nums[i])

            if i == current_end:        # exhausted current jump range — must jump
                jumps      += 1
                current_end = farthest  # extend range to farthest reachable point

        return jumps


# ===== Test Cases =====
if __name__ == "__main__":
    brute   = SolutionBrute()
    dp      = SolutionDP()
    greedy  = SolutionGreedy()

    test_cases = [
        ([2, 3, 1, 1, 4], 2),
        ([2, 3, 0, 1, 4], 2),
        ([1],             0),
        ([1, 2],          1),
        ([1, 1, 1, 1],    3),
        ([4, 1, 1, 1, 1], 1),
    ]

    for nums, expected in test_cases:
        r1 = brute.jump(nums[:])
        r2 = dp.jump(nums[:])
        r3 = greedy.jump(nums[:])
        status = "PASS" if r1 == expected and r2 == expected and r3 == expected else "FAIL"
        print(f"{status} nums={nums} -> brute={r1}, dp={r2}, greedy={r3} (expected {expected})")
