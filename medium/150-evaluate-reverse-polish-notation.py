"""
150. Evaluate Reverse Polish Notation

Evaluate an arithmetic expression given in Reverse Polish Notation (Postfix).
Operators come AFTER their operands — no parentheses needed, no ambiguity.

Valid operators: '+', '-', '*', '/'
- Division truncates toward zero (not floor division)
- All intermediate values fit in a 32-bit integer

Example 1:  ["2","1","+","3","*"]  → ((2 + 1) * 3) = 9
Example 2:  ["4","13","5","/","+"] → (4 + (13 / 5)) = 6
Example 3:  ["10","6","9","3","+","-11","*","/","*","17","+","5","+"] → 22

Constraints:
- 1 <= tokens.length <= 10^4
- tokens[i] is either an operator or an integer in [-200, 200]

Key idea: Use a stack — push numbers, on operator pop two, compute, push result.
"""

# ===== My Original Solution =====
# Stack-based. For each token: if operator, pop two operands, compute, push result.
# Uses int(float(a)/b) for division to handle truncation toward zero correctly.
# Time: O(n) | Space: O(n)

class SolutionOriginal(object):
    def evalRPN(self, tokens):
        if not tokens:
            return 0

        stack = []
        ops = "-+*/"

        for token in tokens:
            if token in ops:
                b = stack.pop()             # second operand (pushed last)
                a = stack.pop()             # first operand
                result = 0
                if token == "+":
                    result = a + b
                elif token == "-":
                    result = a - b
                elif token == "*":
                    result = a * b
                else:
                    result = int(float(a) / b)  # truncate toward zero (handles negatives)
                stack.append(result)
            else:
                stack.append(int(token))    # convert string to int and push

        return stack[-1]                    # final result is the only element left


# ===== Optimized Solution (operator map + int() truncation) =====
# Same O(n) logic but maps operators to lambdas — eliminates if/elif chain.
# Uses int(a/b) with Python's true division for clean truncation toward zero.
# Time: O(n) | Space: O(n)

class SolutionOptimized(object):
    def evalRPN(self, tokens):
        ops = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: int(a / b),   # int() truncates toward zero (not floor)
        }

        stack = []

        for token in tokens:
            if token in ops:
                b = stack.pop()             # second operand
                a = stack.pop()             # first operand
                stack.append(ops[token](a, b))
            else:
                stack.append(int(token))

        return stack[0]


# ===== Test Cases =====
if __name__ == "__main__":
    original  = SolutionOriginal()
    optimized = SolutionOptimized()

    test_cases = [
        (["2","1","+","3","*"],                                             9),
        (["4","13","5","/","+"],                                            6),
        (["10","6","9","3","+","-11","*","/","*","17","+","5","+"],        22),
        (["3","-4","/"],                                                    0),   # truncates toward zero → 0 not -1
        (["-3","4","/"],                                                    0),   # same
    ]

    for tokens, expected in test_cases:
        r1 = original.evalRPN(tokens[:])
        r2 = optimized.evalRPN(tokens[:])
        status = "PASS" if r1 == expected and r2 == expected else "FAIL"
        print(f"{status} tokens={tokens} -> original={r1}, optimized={r2} (expected {expected})")
