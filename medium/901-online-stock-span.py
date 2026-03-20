# 901. Online Stock Span (Medium)
# Tags: Monotonic Stack
#
# For each day's price, return how many consecutive days (going backward, including today)
# the price was <= today's price. This is called the "span".
#
# Example: prices [100, 80, 60, 70, 60, 75, 85] → spans [1, 1, 1, 2, 1, 4, 6]


# ─────────────────────────────────────────────
# BRUTE FORCE — O(n) per call, O(n) space
# ─────────────────────────────────────────────
# Store all prices seen so far. For each new price, walk backwards
# counting consecutive days where price <= today's price.
# Simple but recomputes from scratch every call.

class StockSpanner(object):

    def __init__(self):
        self.prices = []

    def next(self, price):
        self.prices.append(price)
        span = 0
        # walk backwards through all stored prices
        for p in reversed(self.prices):
            if p <= price:
                span += 1
            else:
                break   # first day with a higher price breaks the streak
        return span


# ─────────────────────────────────────────────
# FIRST SOLUTION — Stack with span jumps — O(1) amortized, O(n) space
# ─────────────────────────────────────────────
# Key insight: store [price, span] pairs in the stack.
# When querying, instead of walking day-by-day, JUMP over entire spans
# of already-computed ranges using the stored span values.
#
# For new price, start at the last element and jump backwards:
#   right pointer moves: right -= stack[right][1]  (skips a whole block)
# This avoids re-scanning elements that were already grouped.
#
# The final span = (total elements in stack) - right
# Then push [price, span] for future use.
#
# Downside: does NOT pop elements from stack (they accumulate forever),
# and the pointer-jumping can still be O(n) in the worst case per call
# (e.g. strictly decreasing prices, then one huge price).

class StockSpanner2(object):

    def __init__(self):
        self.stack = []  # each entry: [price, span]

    def next(self, price):
        if not self.stack:
            self.stack.append([price, 1])
            return 1

        n = len(self.stack)
        right = n - 1  # start at the most recent element

        # jump backwards using stored spans to skip already-grouped ranges
        while right > -1 and self.stack[right][0] <= price:
            right -= self.stack[right][1]   # jump over this element's entire span

        # everything from index (right+1) to (n-1) was <= price
        # +1 for today itself
        res = n - right
        self.stack.append([price, res])
        return res


# ─────────────────────────────────────────────
# OPTIMAL — Monotonic Stack with popping — O(1) amortized, O(n) space
# ─────────────────────────────────────────────
# Same [price, span] idea but we actually POP elements from the stack
# instead of jumping over them with a pointer.
#
# When a new price comes in:
#   - pop from the stack any entry with price <= today's price
#   - accumulate their spans into today's span (they're all dominated by today)
#   - push (today's price, accumulated span)
#
# Why this is better: old dominated elements are gone forever → true O(1) amortized.
# Each element is pushed once and popped at most once across all calls.
#
# Stack stays monotonically DECREASING (front to back: highest to lowest).
# The top of the stack is always the most recent "blocking" price (higher than today).

class StockSpanner3(object):

    def __init__(self):
        self.stack = []  # stores (price, span); top = most recent higher price

    def next(self, price):
        span = 1  # today always counts as 1

        # pop all entries with price <= today — absorb their spans
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]   # add the popped element's span to ours

        # push today: future prices will pop this when they dominate it
        self.stack.append((price, span))
        return span


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
