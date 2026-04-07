# 322. Coin Change
# https://leetcode.com/problems/coin-change/
#
# You are given an integer array coins representing coins of different
# denominations and an integer amount representing a total amount of money.
# Return the fewest number of coins needed to make up that amount.
# If that amount cannot be made up by any combination of the coins, return -1.
# You may assume you have an infinite number of each kind of coin.
#
# Example 1:
#   Input: coins = [1,2,5], amount = 11
#   Output: 3  (11 = 5 + 5 + 1)
#
# Example 2:
#   Input: coins = [2], amount = 3
#   Output: -1
#
# Example 3:
#   Input: coins = [1], amount = 0
#   Output: 0
#
# Constraints:
#   1 <= coins.length <= 12
#   1 <= coins[i] <= 2^31 - 1
#   0 <= amount <= 10^4
from collections import deque


# Brute Force (Pure DFS) - O(k^amount) time
# Try subtracting every coin from the remaining amount recursively.
# No caching — every subproblem is recomputed from scratch, which causes
# exponential blowup. Correct but TLEs on large inputs.
class SolutionBrute:
    def coinChange(self, coins, amount):
        def dfs(remaining):
            if remaining == 0:
                return 0                       # exact change made, 0 more coins needed
            if remaining < 0:
                return float('inf')            # overshot — this path is invalid

            res = float('inf')
            for coin in coins:
                res = min(res, dfs(remaining - coin) + 1)  # try each coin, keep minimum

            return res

        ans = dfs(amount)
        return ans if ans != float('inf') else -1


# DFS + Pruning (Backtracking) - still exponential, but much faster in practice
# Sort coins descending so we try the largest coins first (fewer coins = deeper pruning).
# For each coin denomination, try using it k times (max possible down to 0).
# If our current count already meets or exceeds the best known answer, prune that branch.
class SolutionPruning:
    def coinChange(self, coins, amount):
        self.res = float('inf')
        coins.sort(reverse=True)  # largest coins first for aggressive pruning

        def dfs(i, remaining, count):
            if remaining == 0:
                self.res = min(self.res, count)  # found a valid combo, update best
                return
            if i == len(coins):
                return  # exhausted all denominations with leftover — dead end

            coin = coins[i]
            max_use = remaining // coin  # max times we can use this coin

            # try using k copies of coins[i], from max down to 0
            for k in range(max_use, -1, -1):
                if count + k >= self.res:
                    break                        # pruning: can't beat current best
                dfs(i + 1, remaining - k * coin, count + k)

        dfs(0, amount, 0)
        return self.res if self.res != float('inf') else -1


# BFS (Shortest Path) - O(amount × len(coins)) time, O(amount) space
# Model the problem as a graph: each node is a remaining amount, each edge is
# subtracting a coin. BFS naturally finds the shortest path (fewest coins) to 0.
# visited set prevents re-processing the same amount at a deeper level.
class SolutionBFS:
    def coinChange(self, coins, amount):
        if amount == 0:
            return 0

        queue = deque([(amount, 0)])  # (remaining amount, coins used so far)
        visited = {amount}

        while queue:
            curr, steps = queue.popleft()

            for coin in coins:
                nxt = curr - coin

                if nxt == 0:
                    return steps + 1            # reached 0 — this is the shortest path

                if nxt > 0 and nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, steps + 1))

        return -1  # queue exhausted without reaching 0


# Top-Down DP (DFS + Memoization) - O(amount × len(coins)) time, O(amount) space
# Same recursion as brute force, but cache each subproblem in memo so it's only
# solved once. "How many coins to make amount X?" is computed at most once per X.
class SolutionTopDown:
    def coinChange(self, coins, amount):
        memo = {}

        def dfs(rem):
            if rem == 0:
                return 0
            if rem < 0:
                return float('inf')
            if rem in memo:
                return memo[rem]               # already solved this subproblem

            res = float('inf')
            for coin in coins:
                res = min(res, dfs(rem - coin) + 1)

            memo[rem] = res                    # cache before returning
            return res

        ans = dfs(amount)
        return ans if ans != float('inf') else -1


# Bottom-Up DP (Optimal) - O(amount × len(coins)) time, O(amount) space
# Build the answer iteratively from 0 up to amount.
# dp[i] = fewest coins needed to make amount i.
# For each amount i, try every coin: if we use that coin, we need dp[i - coin] + 1 coins.
# dp[0] = 0 is the base case (0 coins needed to make amount 0).
class Solution:
    def coinChange(self, coins, amount):
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0  # base case: 0 coins to make amount 0

        for i in range(1, amount + 1):
            for coin in coins:
                if i - coin >= 0:             # coin is small enough to use
                    dp[i] = min(dp[i], dp[i - coin] + 1)

        return dp[amount] if dp[amount] != float('inf') else -1


coins = [1, 2, 5]
amount = 11
sol = Solution()
print(sol.coinChange(coins, amount))  # 3
