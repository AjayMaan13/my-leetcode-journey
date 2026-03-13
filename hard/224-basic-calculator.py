"""
LeetCode 224. Basic Calculator  |  Hard

Given a string s representing a valid expression with '+', '-', '(', ')', and
spaces, evaluate and return the result. No eval() allowed.

Examples:
    "1 + 1"          → 2
    " 2-1 + 2 "      → 3
    "(1+(4+5+2)-3)+(6+8)" → 23

Constraints:
    Only '+', '-', '(', ')', digits, and spaces (no '*' or '/').
    '-' may be used as a unary operator.
"""


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 1: Recursive — extract substrings for each bracket pair
# Time  : O(n²),  Space : O(n)  (recursion depth × substring copying)
#
# Idea:
#   Scan left to right. When we hit '(', find its matching ')' manually,
#   slice out the inner string, and RECURSE on it to get its value.
#   That value becomes `num` at the current level.
#
# Uses the same operator-flushing logic as Approach 2 (res list + prev op),
# but delegates '(' handling to a recursive call instead of a stack.
#
# Drawback: finding the matching ')' is O(n) per bracket pair, and substring
# slicing copies memory → O(n²) overall for deeply nested expressions.
# ─────────────────────────────────────────────────────────────────────────────
def calculate_recursive(s):
    if not s:
        return 0

    num  = 0
    prev = "+"
    res  = []
    i    = 0

    while i < len(s):
        ch = s[i]

        if ch.isdigit():
            num = num * 10 + int(ch)    # build multi-digit number

        if ch == "(":
            # find the matching closing bracket (handle nested brackets)
            start        = i
            end          = start + 1
            bracket_open = 0

            while s[end] != ")" or bracket_open != 0:
                if s[end] == "(":
                    bracket_open += 1
                elif s[end] == ")" and bracket_open > 0:
                    bracket_open -= 1
                end += 1

            # recurse on the inner expression (without the outer parentheses)
            num = calculate_recursive(s[start + 1 : end])
            i   = end   # jump i to the closing ')'

        if ch in "+-" or i == len(s) - 1:
            # flush num into res using the last operator
            if prev == "+":
                res.append(num)
            elif prev == "-":
                res.append(-num)

            prev = ch
            num  = 0

        i += 1

    return sum(res)


# ─────────────────────────────────────────────────────────────────────────────
# APPROACH 2: Single-pass Stack  ← OPTIMAL
# Time  : O(n),  Space : O(n)
#
# Key insight:
#   We never need to store the full inner string — just save and restore
#   the current (res, prev) state on a stack whenever we enter a bracket.
#
# Three variables at each depth level:
#   res  — list of numbers accumulated so far at this depth
#   prev — last operator seen at this depth (determines how to flush num)
#   num  — current number being built
#
# On '(':  push (res, prev) onto stack → reset res=[], prev='+', num=0
# On ')':  flush last num, sum up inner res → that sum becomes `num`
#          for the parent level, then pop (res, prev) to restore parent
# On operator or end-of-string: flush num into res using prev, update prev
#
# Every character is visited exactly once → O(n).
#
# Trace: "(1+(4+5+2)-3)+(6+8)"
#   '(' → push ([], '+'), reset
#   '1' → num=1
#   '+' → flush: res=[1], prev='+'
#   '(' → push ([1],'+'), reset
#   '4' → num=4
#   '+' → flush: res=[4], prev='+'
#   '5' → num=5
#   '+' → flush: res=[4,5], prev='+'
#   '2' → num=2
#   ')' → flush: res=[4,5,2] → sum=11 → num=11
#          pop → res=[1], prev='+' → (will flush 11 next)
#   '-' → flush num=11: res=[1,11], prev='-'
#   '3' → num=3
#   ')' → flush num=3: res=[1,11,-3] → sum=9 → num=9
#          pop → res=[], prev='+' → (will flush 9 next)
#   '+' → flush num=9: res=[9], prev='+'
#   '(' → push ([9],'+'), reset
#   '6' → num=6
#   '+' → flush: res=[6], prev='+'
#   '8' → num=8
#   end → flush: res=[6,8]
#   ')' → sum=14 → num=14, pop → res=[9], prev='+'
#   end of string: flush num=14 → res=[9,14]
#   return sum([9,14]) = 23  ✓
# ─────────────────────────────────────────────────────────────────────────────
class Solution(object):
    def calculate(self, s):
        if not s:
            return 0

        stack = []      # each entry: (res, prev) saved when entering '('
        res   = []      # numbers accumulated at current depth
        prev  = "+"     # last operator seen (start with '+' so first num is added)
        num   = 0
        i     = 0

        while i < len(s):
            ch = s[i]

            # build multi-digit number character by character
            if ch.isdigit():
                num = num * 10 + int(ch)

            # open bracket: freeze current state, start fresh for inner expr
            elif ch == "(":
                stack.append((res, prev))
                res  = []
                prev = "+"
                num  = 0

            # flush on: operator, close bracket, or last character
            if ch in "+-" or ch == ")" or i == len(s) - 1:

                # apply prev operator to push num into current res
                if prev == "+":
                    res.append(num)
                elif prev == "-":
                    res.append(-num)

                # close bracket: collapse inner result, restore parent state
                if ch == ")":
                    num       = sum(res)        # inner expression evaluated
                    res, prev = stack.pop()     # restore parent (res, prev)
                    # num now holds the bracket result and will be flushed
                    # when the NEXT operator (or end) is encountered
                    i += 1
                    continue                    # skip the prev/num reset below

                prev = ch
                num  = 0

            i += 1

        return sum(res)
