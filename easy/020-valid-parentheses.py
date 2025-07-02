"""
20. Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', 
determine if the input string is valid.

An input string is valid if:
- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.

Example:
Input: s = "({[]})"
Output: True

Constraints:
- 1 <= s.length <= 10^4
- s consists of parentheses only '()[]{}'.
"""

# ✅ My Solution
class SolutionOriginal(object):
    def isValid(self, s):
        if len(s) % 2 != 0:
            return False
        
        opening = set('([{')
        matches = set([('(', ')'), ('[', ']'), ('{', '}')])

        stack = []

        for paren in s:
            if paren in opening:
                stack.append(paren)
            else:
                if not stack:
                    return False
                last_open = stack.pop()
                if (last_open, paren) not in matches:
                    return False

        return len(stack) == 0


# ✅ Optimized Solution (Dictionary Mapping)
class SolutionOptimized(object):
    def isValid(self, s):
        stack = []
        bracket_map = {')': '(', '}': '{', ']': '['}

        for char in s:
            if char in bracket_map:
                top_element = stack.pop() if stack else '#'
                if bracket_map[char] != top_element:
                    return False
            else:
                stack.append(char)

        return not stack


# ✅ Test Cases
if __name__ == "__main__":
    original = SolutionOriginal()
    optimized = SolutionOptimized()

    test_cases = [
        ("()", True),
        ("()[]{}", True),
        ("(]", False),
        ("([)]", False),
        ("{[]}", True),
        ("((()))", True),
        ("(((((", False),
        ("", True),
        ("[", False),
        ("({[]})", True)
    ]

    print("Testing SolutionOriginal:")
    for s, expected in test_cases:
        result = original.isValid(s)
        print(f"isValid({s!r}) = {result} (Expected: {expected})")

    print("\nTesting SolutionOptimized:")
    for s, expected in test_cases:
        result = optimized.isValid(s)
        print(f"isValid({s!r}) = {result} (Expected: {expected})")
