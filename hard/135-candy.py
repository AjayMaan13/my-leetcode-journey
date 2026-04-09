# 135. Candy
# https://leetcode.com/problems/candy/
#
# There are n children standing in a line. Each child is assigned a rating value.
# You must give candies to these children such that:
#   - Each child must have at least 1 candy.
#   - Children with a higher rating than a neighbor get more candies than that neighbor.
# Return the minimum total number of candies needed.
#
# Example 1:
#   Input: ratings = [1,0,2]
#   Output: 5  (allocate [2,1,2])
#
# Example 2:
#   Input: ratings = [1,2,2]
#   Output: 4  (allocate [1,2,1] — equal ratings don't need equal candies)
#
# Constraints:
#   n == ratings.length
#   1 <= n <= 2 * 10^4
#   0 <= ratings[i] <= 2 * 10^4


# Wrong Approach (for learning) — trying to fix descending slopes in-place
# The idea was: when we hit a decreasing slope and the previous child only has 1 candy,
# walk back and increment earlier children to make room.
# Problem: this double-counts increments during backtracking and misses cases where
# the ascending pass already gave enough candies. One-pass fixes don't cleanly handle
# the interaction between left and right constraints simultaneously.
class SolutionWrong:
    def candy(self, ratings):
        rates = [1] * len(ratings)

        for i in range(1, len(ratings)):
            if ratings[i] > ratings[i - 1]:
                rates[i] = rates[i - 1] + 1
            elif ratings[i] < ratings[i - 1]:
                if rates[i - 1] == 1:
                    # BUG: walks back and increments while also not updating rates[i],
                    # so the descending child still gets 1 even when it shouldn't.
                    peak = i
                    while peak > -1 and ratings[peak - 1] > ratings[peak]:
                        peak -= 1
                        rates[peak] += 1

        return sum(rates)


# Greedy (Two-Pass) - O(n) time, O(n) space
# Key insight: left and right neighbor constraints can be satisfied independently,
# then combined with max().
#
# Pass 1 (Left → Right):
#   If ratings[i] > ratings[i-1], child i needs more than child i-1.
#   Set candies[i] = candies[i-1] + 1. Otherwise leave it at 1.
#   This satisfies all LEFT neighbor constraints.
#
# Pass 2 (Right → Left):
#   If ratings[i] > ratings[i+1], child i needs more than child i+1.
#   Set candies[i] = max(candies[i], candies[i+1] + 1).
#   We take the max so we don't undo the left-pass result.
#   This satisfies all RIGHT neighbor constraints.
#
# Why two passes? A single left-to-right pass misses cases like [3,2,1] where
# later children's needs ripple backwards. The right-to-left pass catches these.
class Solution:
    def candy(self, ratings):
        n = len(ratings)
        candies = [1] * n  # start: every child gets 1 candy

        # Pass 1: enforce left-neighbor constraint
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        # Pass 2: enforce right-neighbor constraint without breaking left-pass results
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)


ratings = [1, 0, 2]
sol = Solution()
print(sol.candy(ratings))  # 5

ratings = [1, 2, 2]
print(sol.candy(ratings))  # 4

ratings = [1, 2, 3, 1, 0]
print(sol.candy(ratings))  # 11  ([1,2,3,2,1])
