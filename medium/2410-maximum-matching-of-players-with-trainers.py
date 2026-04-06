# 2410. Maximum Matching of Players With Trainers
# https://leetcode.com/problems/maximum-matching-of-players-with-trainers/
#
# You are given a 0-indexed integer array players, where players[i] represents
# the ability of the ith player. You are also given a 0-indexed integer array
# trainers, where trainers[j] represents the training capacity of the jth trainer.
#
# The ith player can match with the jth trainer if the player's ability is less
# than or equal to the trainer's training capacity. Additionally, the ith player
# can be matched with at most one trainer, and the jth trainer can be matched
# with at most one player.
#
# Return the maximum number of matchings between players and trainers that
# satisfy these conditions.
#
# Example 1:
#   Input: players = [4,7,9], trainers = [8,2,5,8]
#   Output: 2
#   Explanation: players[0] matches trainers[0] (4 <= 8), players[1] matches
#   trainers[3] (7 <= 8). 2 is the maximum number of matchings.
#
# Example 2:
#   Input: players = [1,1,1], trainers = [10]
#   Output: 1
#   Explanation: The trainer can match any of the 3 players, but only one match
#   is possible since there is only one trainer.
#
# Constraints:
#   1 <= players.length, trainers.length <= 10^5
#   1 <= players[i], trainers[j] <= 10^9


# Greedy (Two Pointers) - O(n log n) time, O(1) space
# Sort both arrays. Try to match the weakest unmatched player with the smallest
# capable trainer. If the trainer can handle the player, match them and advance
# both pointers. Otherwise, try a bigger trainer for the same player.
class Solution:
    def matchPlayersAndTrainers(self, players, trainers):
        if not players or not trainers:
            return 0

        players.sort()
        trainers.sort()

        count = i = j = 0

        while i < len(players) and j < len(trainers):
            if players[i] <= trainers[j]:  # trainer j can handle player i
                count += 1
                i += 1                     # player matched, move to next player
            j += 1                         # always try next trainer

        return count


players = [4, 7, 9]
trainers = [8, 2, 5, 8]
sol = Solution()
print(sol.matchPlayersAndTrainers(players, trainers))  # 2
