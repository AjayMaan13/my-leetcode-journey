"""
355. Design Twitter
https://leetcode.com/problems/design-twitter/
Difficulty: Medium
Topics: Hash Table, Linked List, Design, Heap (Priority Queue)

Problem:
    Design a simplified Twitter with:
      - postTweet(userId, tweetId)   — user posts a tweet
      - getNewsFeed(userId)          — 10 most recent tweets from self + followed users
      - follow(followerId, followeeId)
      - unfollow(followerId, followeeId)

Example:
    postTweet(1, 5)       →  user 1 posts tweet 5
    getNewsFeed(1)        →  [5]
    follow(1, 2)          →  user 1 follows user 2
    postTweet(2, 6)       →  user 2 posts tweet 6
    getNewsFeed(1)        →  [6, 5]
    unfollow(1, 2)
    getNewsFeed(1)        →  [5]

Constraints:
    1 <= userId, followerId, followeeId <= 500
    0 <= tweetId <= 10^4
    At most 3 * 10^4 calls total
"""

import heapq
from collections import defaultdict


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: YOUR SOLUTION — Global Tweet List (TLE)
# ─────────────────────────────────────────────────────────────────────────────
# Idea:
#   Store ALL tweets in a single global list in posting order.
#   For getNewsFeed, scan the list backwards and collect tweets from
#   the user and their followees until we have 10.
#
# Why it TLEs:
#   getNewsFeed is O(T) where T = total tweets ever posted (up to 3*10^4).
#   With 3*10^4 calls to getNewsFeed, worst case is O(T * Q) = O(9 * 10^8).
#   The `user in users` check is also O(F) per tweet (list membership),
#   where F = number of followees — should be a set for O(1) lookup.
#
# Fix for the list-membership issue (minor):
#   Change `users` from a list to a set → O(1) lookup instead of O(F).
#   But the fundamental O(T) scan per query still causes TLE at scale.
#
# Time:  postTweet O(1) | getNewsFeed O(T) ← bottleneck | follow/unfollow O(F)
# Space: O(T) — global tweet list
# ─────────────────────────────────────────────────────────────────────────────

class Twitter_TLE:
    def __init__(self):
        self.follows = {}          # {followerId: [followeeId, ...]}
        self.tweets = []           # [(userId, tweetId)] in posting order

    def postTweet(self, userId, tweetId):
        self.tweets.append((userId, tweetId))

    def getNewsFeed(self, userId):
        count = 0
        # BUG: users is a list → `user in users` is O(F) per tweet
        # FIX: use a set for O(1) membership
        users = set(self.follows.get(userId, []))
        users.add(userId)

        res = []
        for i in range(len(self.tweets) - 1, -1, -1):   # scan backwards: O(T)
            if count == 10:
                break
            user, postid = self.tweets[i]
            if user in users:
                res.append(postid)
                count += 1
        return res

    def follow(self, followerId, followeeId):
        self.follows.setdefault(followerId, []).append(followeeId)

    def unfollow(self, followerId, followeeId):
        following = self.follows.get(followerId, [])
        if followeeId in following:
            following.remove(followeeId)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: OPTIMAL — Per-User Tweet Lists + Min-Heap Merge
# ─────────────────────────────────────────────────────────────────────────────
# Core insight from your second (partially OCR'd) solution:
#   Instead of one global list, store tweets PER USER.
#   Then getNewsFeed becomes a k-way merge of the most recent tweets
#   from each followed user's list — using a min-heap.
#
# Key design decisions:
#
#   tweetMap : {userId: [(timestamp, tweetId), ...]}
#     Each user's tweets stored in chronological order.
#     We always look at the LAST element (most recent) first.
#
#   followMap : {userId: set(followeeIds)}
#     Set for O(1) follow/unfollow and membership check.
#     User always implicitly follows themselves (added in getNewsFeed).
#
#   timestamp : global counter, decremented on each postTweet
#     Using negative values means min-heap naturally gives us
#     the most recent tweet first (smallest negative = most recent).
#
# getNewsFeed algorithm (k-way merge):
#   1. For each followee (+ self), seed the heap with their most recent tweet.
#      Heap entry: (timestamp, tweetId, followeeId, prev_index)
#   2. Pop the most recent tweet (min timestamp = most negative = newest).
#   3. If that followee has more tweets, push their next most recent.
#   4. Repeat until heap empty or we have 10 tweets.
#
#   This is the same pattern as "Merge K Sorted Lists" (LC 23).
#
# Time:
#   postTweet   O(1)
#   getNewsFeed O(F log F + 10 log F) = O(F log F)  where F = followees
#   follow      O(1)
#   unfollow    O(1)
#
# Space: O(T + U*F)  — tweets per user + follow graph
# ─────────────────────────────────────────────────────────────────────────────

class Twitter:
    def __init__(self):
        self.timestamp = 0                           # global clock, decremented each tweet
        self.tweetMap = defaultdict(list)            # {userId: [(timestamp, tweetId), ...]}
        self.followMap = defaultdict(set)            # {userId: {followeeId, ...}}

    def postTweet(self, userId, tweetId):
        self.timestamp -= 1                          # decrement → more negative = more recent
        self.tweetMap[userId].append((self.timestamp, tweetId))

    def getNewsFeed(self, userId):
        res = []
        min_heap = []                                # min-heap: (timestamp, tweetId, followeeId, index)

        self.followMap[userId].add(userId)           # always include own tweets

        for followeeId in self.followMap[userId]:
            if followeeId in self.tweetMap:
                tweets = self.tweetMap[followeeId]
                index = len(tweets) - 1              # start from most recent
                ts, tweetId = tweets[index]
                heapq.heappush(min_heap, (ts, tweetId, followeeId, index - 1))

        while min_heap and len(res) < 10:
            ts, tweetId, followeeId, index = heapq.heappop(min_heap)
            res.append(tweetId)
            if index >= 0:                           # followee has older tweets
                ts2, tweetId2 = self.tweetMap[followeeId][index]
                heapq.heappush(min_heap, (ts2, tweetId2, followeeId, index - 1))

        return res

    def follow(self, followerId, followeeId):
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId, followeeId):
        self.followMap[followerId].discard(followeeId)   # discard: no KeyError if missing


# ─────────────────────────────────────────────────────────────────────────────
# TESTS
# ─────────────────────────────────────────────────────────────────────────────

def run_tests():
    all_passed = True

    def check(label, got, expected):
        nonlocal all_passed
        if got != expected:
            all_passed = False
            print(f"  ✗ FAIL | {label} | got {got}, expected {expected}")

    # ── Test 1: LeetCode example ──────────────────────────────────────────────
    for cls in [Twitter_TLE, Twitter]:
        t = cls()
        t.postTweet(1, 5)
        check(f"{cls.__name__} ex1-a", t.getNewsFeed(1), [5])
        t.follow(1, 2)
        t.postTweet(2, 6)
        check(f"{cls.__name__} ex1-b", t.getNewsFeed(1), [6, 5])
        t.unfollow(1, 2)
        check(f"{cls.__name__} ex1-c", t.getNewsFeed(1), [5])

    # ── Test 2: Feed capped at 10 ─────────────────────────────────────────────
    for cls in [Twitter_TLE, Twitter]:
        t = cls()
        for i in range(15):
            t.postTweet(1, i)
        feed = t.getNewsFeed(1)
        check(f"{cls.__name__} cap10-len",   len(feed), 10)
        check(f"{cls.__name__} cap10-order", feed, list(range(14, 4, -1)))  # 14..5

    # ── Test 3: Merge tweets from multiple followees ──────────────────────────
    for cls in [Twitter_TLE, Twitter]:
        t = cls()
        t.postTweet(1, 10)
        t.postTweet(2, 20)
        t.postTweet(3, 30)
        t.follow(1, 2)
        t.follow(1, 3)
        check(f"{cls.__name__} merge", t.getNewsFeed(1), [30, 20, 10])

    # ── Test 4: Unfollow removes tweets from feed ─────────────────────────────
    for cls in [Twitter_TLE, Twitter]:
        t = cls()
        t.postTweet(1, 1)
        t.postTweet(2, 2)
        t.follow(1, 2)
        check(f"{cls.__name__} follow",   t.getNewsFeed(1), [2, 1])
        t.unfollow(1, 2)
        check(f"{cls.__name__} unfollow", t.getNewsFeed(1), [1])

    # ── Test 5: User with no tweets ───────────────────────────────────────────
    for cls in [Twitter_TLE, Twitter]:
        t = cls()
        check(f"{cls.__name__} empty", t.getNewsFeed(99), [])

    # ── Test 6: User only sees own tweets if following no one ─────────────────
    for cls in [Twitter_TLE, Twitter]:
        t = cls()
        t.postTweet(1, 100)
        t.postTweet(2, 200)
        check(f"{cls.__name__} self-only", t.getNewsFeed(1), [100])

    # ── Test 7: Interleaved tweets from 3 users in correct order ─────────────
    for cls in [Twitter_TLE, Twitter]:
        t = cls()
        t.postTweet(1, 1)   # ts=-1
        t.postTweet(2, 2)   # ts=-2
        t.postTweet(3, 3)   # ts=-3
        t.postTweet(1, 4)   # ts=-4
        t.postTweet(2, 5)   # ts=-5
        t.follow(1, 2)
        t.follow(1, 3)
        # most recent first: 5,4,3,2,1
        check(f"{cls.__name__} interleave", t.getNewsFeed(1), [5, 4, 3, 2, 1])

    if all_passed:
        print("All tests passed ✓")
    else:
        print("\nSome tests FAILED — see above.")


if __name__ == "__main__":
    run_tests()


# ─────────────────────────────────────────────────────────────────────────────
# COMPLEXITY SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
#
# Method          TLE Approach        Optimal Heap Approach
# ──────────────────────────────────────────────────────────────────────────────
# postTweet       O(1)                O(1)
# getNewsFeed     O(T)  ← TLE        O(F log F)  F = followees (≤ 500)
# follow          O(1)                O(1)
# unfollow        O(F)  (list.remove) O(1)        (set.discard)
# Space           O(T)                O(T + U·F)
#
# T = total tweets posted, U = total users, F = followees per user
#
# ─────────────────────────────────────────────────────────────────────────────
# README — Heap Section Update
# ─────────────────────────────────────────────────────────────────────────────
#
# | # | Problem | Difficulty | Approach |
# |---|---------|------------|----------|
# | 355 | Design Twitter | Medium | Per-user tweet lists + k-way merge heap;
# |     |                |        | same pattern as Merge K Sorted Lists (LC 23) |
