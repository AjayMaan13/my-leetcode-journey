# 1423. Maximum Points You Can Obtain from Cards (Medium)
# Tags: Sliding Window, Prefix Sum, Array
#
# Take exactly k cards from either end (left or right).
# Return the maximum total score possible.
#
# Example: cardPoints = [1,2,3,4,5,6,1], k = 3 → 12  (take 5,6,1 from right)


# ─────────────────────────────────────────────
# BRUTE FORCE — O(k) time, O(1) space
# ─────────────────────────────────────────────
# Key observation: we must take k cards total from left and/or right.
# So we try every split: take i from the left, (k-i) from the right, for i in 0..k.
# prefix[i]  = sum of first i cards
# suffix[j]  = sum of last j cards
# For each split, score = prefix[i] + suffix[k-i]

class Solution(object):
    def maxScore(self, cardPoints, k):
        n = len(cardPoints)
        prefix = [0] * (k + 1)   # prefix[i] = sum of cardPoints[0..i-1]
        suffix = [0] * (k + 1)   # suffix[j] = sum of cardPoints[n-j..n-1]

        for i in range(1, k + 1):
            prefix[i] = prefix[i - 1] + cardPoints[i - 1]       # grow from left
            suffix[i] = suffix[i - 1] + cardPoints[n - i]        # grow from right

        res = 0
        for i in range(k + 1):
            res = max(res, prefix[i] + suffix[k - i])  # i from left, k-i from right

        return res


# ─────────────────────────────────────────────
# OPTIMAL — Sliding Window (swap one card at a time) — O(k) time, O(1) space
# ─────────────────────────────────────────────
# Start with all k cards taken from the RIGHT (that's one valid selection).
# Then iteratively swap: give back the rightmost taken card, pick up the next left card.
# Each swap shifts one card from the right pool to the left pool.
# After k swaps we'd have all k from the left — we track the max along the way.
#
# l = index of next left card to pick up (starts at 0)
# r = index of the leftmost right card currently included (starts at n-k)
#
# Each iteration:
#   total += cardPoints[l]   — take one more from left
#   total -= cardPoints[r]   — give back the leftmost of the right cards
#   l, r both advance by 1   — window slides right by one

class Solution2(object):
    def maxScore(self, cardPoints, k):
        n = len(cardPoints)
        l, r = 0, n - k

        total = sum(cardPoints[r:])   # initial score: all k cards from the right
        res = total

        while r < n:
            total += cardPoints[l] - cardPoints[r]   # swap: add left card, drop right card
            res = max(res, total)
            l += 1
            r += 1

        return res
