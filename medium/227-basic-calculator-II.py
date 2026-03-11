"""
227. Basic Calculator II

Evaluate a string expression containing '+', '-', '*', '/' and spaces.
- Integer division truncates toward zero
- No parentheses in this version
- No eval() allowed

Example 1: "3+2*2"     -> 7
Example 2: " 3/2 "     -> 1
Example 3: " 3+5 / 2 " -> 5

Constraints:
- 1 <= s.length <= 3 * 10^5
- s consists of digits, '+', '-', '*', '/', and ' '
- Expression is always valid

Key insight: '*' and '/' have higher precedence than '+' and '-'.
We need to handle this without parentheses.
"""

# ===== My Solution 1: Two-Stack with Precedence =====
# Uses two stacks — nums (operands) and ops (operators).
# Before pushing a new operator, flush all pending ops of >= precedence.
# This correctly handles precedence without converting to postfix first.
# Time: O(n) | Space: O(n)

class SolutionTwoStack(object):
    def calculate(self, s):
        nums = []
        ops  = []
        order = {'+': 1, '-': 1, '*': 2, '/': 2}  # precedence map

        def apply():
            b  = nums.pop()
            a  = nums.pop()
            op = ops.pop()
            if op == '+': nums.append(a + b)
            elif op == '-': nums.append(a - b)
            elif op == '*': nums.append(a * b)
            else:           nums.append(int(a / b))  # truncate toward zero

        i = 0
        while i < len(s):
            if s[i] == ' ':
                i += 1
                continue

            if s[i].isdigit():
                num = 0
                while i < len(s) and s[i].isdigit():  # parse full multi-digit number
                    num = num * 10 + int(s[i])
                    i += 1
                nums.append(num)
                continue

            if s[i] in '+-*/':
                # flush all pending ops with >= precedence before pushing current op
                while ops and order[ops[-1]] >= order[s[i]]:
                    apply()
                ops.append(s[i])

            i += 1

        while ops:      # flush remaining ops
            apply()

        return nums[-1]


# ===== My Solution 2: Single Stack with prev_op =====
# Smarter approach — no need to track operator precedence explicitly.
# Key insight: '+'/'-' push to stack; '*'/'/' modify the top of stack immediately.
# At the end, sum the stack (handles all deferred additions/subtractions).
# Time: O(n) | Space: O(n)

class SolutionOneStack(object):
    def calculate(self, s):
        stack   = []
        num     = 0
        prev_op = '+'   # treat start as if preceded by '+' so first number gets pushed

        for i, ch in enumerate(s):
            if ch.isdigit():
                num = num * 10 + int(ch)    # build multi-digit number

            if ch in '+-*/' or i == len(s) - 1:  # operator or end of string
                if prev_op == '+':
                    stack.append(num)           # push positive number
                elif prev_op == '-':
                    stack.append(-num)          # push negative number
                elif prev_op == '*':
                    stack[-1] *= num            # apply immediately to top
                elif prev_op == '/':
                    stack[-1] = int(stack[-1] / num)  # apply immediately, truncate toward zero

                prev_op = ch    # remember this operator for next number
                num = 0         # reset number accumulator

        return sum(stack)       # sum all deferred additions/subtractions


# ===== Test Cases =====
if __name__ == "__main__":
    two_stack = SolutionTwoStack()
    one_stack = SolutionOneStack()

    test_cases = [
        ("3+2*2",      7),
        (" 3/2 ",      1),
        (" 3+5 / 2 ",  5),
        ("14-3/2",    13),
        ("1*2-3/4+5*6-7*8+9/10",  -24),
        ("100000000/1/2/3",        16666666),
    ]

    for s, expected in test_cases:
        r1 = two_stack.calculate(s)
        r2 = one_stack.calculate(s)
        status = "PASS" if r1 == expected and r2 == expected else "FAIL"
        print(f"{status} s={s!r:30} -> two_stack={r1}, one_stack={r2} (expected {expected})")
