"""
LeetCode 735. Asteroid Collision  |  Medium

Positive = moving right, negative = moving left. Same speed.
Collision only happens when a right-mover is followed by a left-mover.
Smaller explodes; equal size → both explode; same direction → no collision.

Examples:
    [5,10,-5]       → [5,10]     (10 and -5 collide → 10 wins)
    [8,-8]          → []         (both explode)
    [10,2,-5]       → [10]       (2 vs -5 → -5 wins; 10 vs -5 → 10 wins)
    [3,5,-6,2,-1,4] → [-6,2,4]
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: My Solution V1 — Multi-pass with restart
# Time  : O(n²),  Space : O(n)
#
# Repeatedly scan until no collisions happen in a full pass.
# Each pass pops from asteroids, resolves one collision at a time,
# then transfers everything back from stack to asteroids.
# Inefficient: up to O(n) passes each O(n) → O(n²) total.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def asteroidCollision_v1(self, asteroids):
        if not asteroids:
            return []

        stack = []
        while True:
            colFound = 0
            while asteroids:
                cur = asteroids.pop()
                # collision: right-mover in stack meets left-mover cur
                if stack and stack[-1] < 0 and cur > 0:
                    popped = stack.pop()
                    if cur > abs(popped):
                        stack.append(cur)        # cur (right) wins
                    elif cur < abs(popped):
                        stack.append(popped)     # popped (left) wins
                    # equal → both destroyed
                    colFound += 1
                else:
                    stack.append(cur)
            while stack:
                asteroids.append(stack.pop())    # transfer back for next pass
            if colFound == 0:
                break                            # stable — no collisions this pass

        return asteroids


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: My Solution V2 — Single-pass (improved)
# Time  : O(n²) worst case,  Space : O(n)
#
# Still pops from the back of asteroids (right to left) and uses an inner
# while loop to resolve a chain of collisions for one asteroid before moving on.
# Better than V1 (no restart passes) but the pop()+append() pattern isn't ideal.
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def asteroidCollision_v2(self, asteroids):
        if not asteroids:
            return []

        stack = []
        while asteroids:
            equal = False
            cur = asteroids.pop()

            # while cur (right-mover) keeps beating left-movers in stack
            while not equal and stack and stack[-1] < 0 and cur > 0:
                if cur == abs(stack[-1]):
                    stack.pop()                 # both explode
                    equal = True
                elif cur < abs(stack[-1]):
                    equal = True                # cur destroyed, stack top survives
                else:
                    stack.pop()                 # stack top destroyed, cur continues

            if not equal:
                stack.append(cur)

        while stack:
            asteroids.append(stack.pop())       # transfer result back

        return asteroids


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 3: Optimal — Left-to-right single pass  ← CLEANEST
# Time  : O(n),  Space : O(n)
#
# Process asteroids LEFT TO RIGHT. Push each onto stack.
# A collision can only happen when:
#   current asteroid is NEGATIVE (moving left) AND
#   stack top is POSITIVE (moving right)
#
# Inner while loop resolves the chain: a left-mover may destroy multiple
# right-movers before it either dies or survives. Each asteroid is pushed
# and popped at most once → O(n) total.
#
# `alive` flag tracks whether current asteroid is still alive after collisions.
#
# Trace for [10, 2, -5]:
#   asteroid=10: no collision → stack=[10]
#   asteroid=2:  no collision → stack=[10,2]
#   asteroid=-5: collision! top=2, abs(-5)=5 > 2 → 2 destroyed, continue
#                collision! top=10, abs(-5)=5 < 10 → -5 destroyed (alive=False)
#   stack=[10] → return [10]  ✓
#
# Trace for [8, -8]:
#   asteroid=8:  stack=[8]
#   asteroid=-8: collision! top=8, 8==8 → both destroyed (alive=False), stack=[]
#   return []  ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution:
    def asteroidCollision(self, asteroids):
        stack = []

        for asteroid in asteroids:
            alive = True                        # assume current asteroid survives

            # collision condition: left-mover hits right-mover(s) in stack
            while alive and asteroid < 0 and stack and stack[-1] > 0:
                top = stack.pop()

                if top < abs(asteroid):
                    continue                    # right-mover destroyed; left-mover keeps going
                elif top == abs(asteroid):
                    alive = False               # both destroyed
                else:
                    stack.append(top)           # left-mover destroyed; right-mover survives
                    alive = False

            if alive:
                stack.append(asteroid)          # survived all collisions → add to result

        return stack
