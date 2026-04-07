# 678. Valid Parenthesis String
# https://leetcode.com/problems/valid-parenthesis-string/
#
# Given a string s containing only '(', ')' and '*', return true if s is valid.
# Rules:
#   - '(' must have a corresponding ')'
#   - ')' must have a corresponding '('
#   - '(' must come before its matching ')'
#   - '*' can be treated as '(', ')' or "" (empty string)
#
# Example 1:  s = "()"    -> true
# Example 2:  s = "(*)"   -> true
# Example 3:  s = "(*))"  -> true
#
# Constraints:
#   1 <= s.length <= 100
#   s[i] is '(', ')' or '*'


# Brute Force (DFS) - O(3^n) time, O(n) space
# For every '*', branch into 3 possibilities: treat it as '(', ')' or ''.
# Recursively check if any branch leads to a valid string.
# open tracks how many unmatched '(' we currently have.
# If open ever goes negative we've seen too many ')' — prune that branch.
class SolutionBrute:
    def checkValidString(self, s: str) -> bool:
        def dfs(i, open):
            if open < 0:
                return False        # more ')' than '(' seen so far — invalid
            if i == len(s):
                return open == 0   # valid only if all '(' are matched

            if s[i] == '(':
                return dfs(i + 1, open + 1)
            elif s[i] == ')':
                return dfs(i + 1, open - 1)
            else:                  # s[i] == '*' — try all three interpretations
                return (dfs(i + 1, open + 1) or   # '*' as '('
                        dfs(i + 1, open - 1) or   # '*' as ')'
                        dfs(i + 1, open))          # '*' as ""

        return dfs(0, 0)


# Top-Down DP (Memoization) - O(n^2) time, O(n^2) space
# Same recursion as brute force, but cache (index, open) pairs so each
# unique state is only computed once. There are at most n * (n+1) states
# since open can range from 0 to n.
class SolutionTopDown:
    def checkValidString(self, s: str) -> bool:
        memo = {}

        def dfs(i, open):
            if open < 0:
                return False
            if i == len(s):
                return open == 0

            if (i, open) in memo:
                return memo[(i, open)]  # already solved this state

            if s[i] == '(':
                res = dfs(i + 1, open + 1)
            elif s[i] == ')':
                res = dfs(i + 1, open - 1)
            else:
                res = (dfs(i + 1, open + 1) or
                       dfs(i + 1, open - 1) or
                       dfs(i + 1, open))

            memo[(i, open)] = res
            return res

        return dfs(0, 0)


# Bottom-Up DP - O(n^2) time, O(n^2) space
# dp[i][j] = True if the first i characters of s can be valid with exactly
# j unmatched '(' remaining.
# Transition: for each character, derive reachable states from the previous row.
# Answer: dp[n][0] — processed all chars with 0 unmatched '(' left.
class SolutionBottomUp:
    def checkValidString(self, s: str) -> bool:
        n = len(s)
        # dp[j] = can we reach a state with j open parens after processing current chars
        # Use two sets: current and next, to avoid an n×n matrix
        dp = {0}  # before processing any character, 0 open parens

        for i in range(n):
            next_dp = set()

            for open in dp:
                if s[i] == '(':
                    next_dp.add(open + 1)
                elif s[i] == ')':
                    if open > 0:                 # only valid if there's an unmatched '('
                        next_dp.add(open - 1)
                else:                            # '*' — try all three
                    next_dp.add(open + 1)        # treat as '('
                    if open > 0:
                        next_dp.add(open - 1)    # treat as ')'
                    next_dp.add(open)            # treat as ""

            dp = next_dp

        return 0 in dp  # valid if 0 unmatched '(' remain


# Greedy (lo / hi range tracking) - O(n) time, O(1) space
# Key insight: instead of tracking exact open counts, track the RANGE of
# possible open paren counts [lo, hi].
#
#   lo = minimum possible number of unmatched '(' (treat '*' as ')' or "")
#   hi = maximum possible number of unmatched '(' (treat '*' as '(')
#
# For each character:
#   '('  → both lo and hi increase by 1 (definitely one more open paren)
#   ')'  → both lo and hi decrease by 1 (one open paren matched)
#   '*'  → lo decreases (best case: '*' closes an open)
#           hi increases (best case: '*' opens a new one)
#
# If hi < 0 at any point: too many ')' even in the most optimistic case — return False.
# Clamp lo to 0: we can never have a "negative" number of open parens in reality;
#   lo going negative just means '*' can absorb all the extra ')'.
# At the end, lo == 0 means it's possible to have all parens matched.
class Solution:
    def checkValidString(self, s: str) -> bool:
        lo = hi = 0  # [lo, hi] = range of possible unmatched '(' counts

        for c in s:
            if c == '(':
                lo += 1
                hi += 1
            elif c == ')':
                lo -= 1
                hi -= 1
            else:              # c == '*'
                lo -= 1        # most conservative: treat '*' as ')'
                hi += 1        # most optimistic:   treat '*' as '('

            if hi < 0:
                return False   # even the best case has too many ')' — impossible

            lo = max(lo, 0)    # clamp: open count can't go below 0

        return lo == 0         # valid if 0 unmatched '(' is achievable


s = "()"
sol = Solution()
print(sol.checkValidString(s))   # True

s = "(*)"
print(sol.checkValidString(s))   # True

s = "(*))"
print(sol.checkValidString(s))   # True
