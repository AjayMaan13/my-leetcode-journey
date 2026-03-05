"""
282. EXPRESSION ADD OPERATORS

Problem Statement:
Given a string num (only digits) and an integer target, return all possibilities 
to insert binary operators '+', '-', and/or '*' between digits so that the 
resultant expression evaluates to target.

Note: 
- Operands should not contain leading zeros
- A number can contain multiple digits

Example 1:
Input: num = "123", target = 6
Output: ["1*2*3","1+2+3"]

Example 2:
Input: num = "232", target = 8
Output: ["2*3+2","2+3*2"]

Example 3:
Input: num = "3456237490", target = 9191
Output: []

Constraints:
* 1 <= num.length <= 10
* num consists of only digits
* -2^31 <= target <= 2^31 - 1
"""


# ==============================================================================
# YOUR SOLUTION 1: TLE (TIME LIMIT EXCEEDED)
# ==============================================================================
# Time Complexity: O(4^n * n) - 4 choices per gap, eval() is O(n)
# Space Complexity: O(n) - recursion stack

class Solution_TLE:
    def addOperators(self, num, target):
        """
        Generate all possible expressions, then eval() each one.
        
        Strategy:
        1. Between each pair of digits, choose: +, -, *, or ""
        2. "" means concatenate digits (multi-digit number)
        3. Build string expression and eval() it
        4. Check if result equals target
        
        Why TLE:
        ❌ eval() is expensive - parses and evaluates entire expression
        ❌ Builds string for every possibility (even invalid ones)
        ❌ No pruning - explores all 4^(n-1) combinations
        ❌ Leading zero check happens but still wastes time on invalid paths
        
        This is the "brute force" approach.
        Works for small inputs but too slow for n=10.
        """
        if not num:
            return []

        # "" means no operator → concat digits into multi-digit number
        ops = ["*", "+", "-", ""]

        def makeString(order):
            """Build expression string from operator choices"""
            st = []
            for i in range(len(num) - 1):
                st.append(num[i])
                st.append(order[i])
            st.append(num[-1])
            return "".join(st)

        def backtrack(index, operand_start, order, res):
            """Try all operator combinations"""
            # Base case: placed operators between all digits
            if index == len(num) - 1:
                s = makeString(order)
                if eval(s) == target:  # ← EXPENSIVE!
                    res.append(s)
                    return True
                return False

            # Allow all 4 options by default
            end = len(ops)

            # Leading zero guard:
            # If current operand starts with "0", don't allow ""
            # because ""+"X" would create "0X" (leading zero)
            if num[operand_start] == "0":
                end -= 1  # Remove "" option

            for i in range(end):
                order.append(ops[i])

                if ops[i] == "":
                    # Concat: current operand grows
                    backtrack(index + 1, operand_start, order, res)
                else:
                    # Real operator: next operand starts fresh
                    backtrack(index + 1, index + 1, order, res)

                order.pop()  # Backtrack

        res = []
        backtrack(0, 0, [], res)
        return res


# ==============================================================================
# YOUR SOLUTION 2: OPTIMAL (TRACK EVALUATION STATE)
# ==============================================================================
# Time Complexity: O(4^n) - 4 choices per position
# Space Complexity: O(n) - recursion stack
#
# This is the OPTIMAL solution! ⭐

class Solution:
    def addOperators(self, num, target):
        """
        Track evaluation state during backtracking - NO eval()!
        
        Key Innovation: Track `cur` and `prev` during recursion
        - cur: current result of expression so far
        - prev: last term added (needed for multiplication!)
        
        Why `prev` is critical:
        Expression: 1 + 2 * 3
        
        Without tracking prev:
        1 + 2 = 3, then 3 * 3 = 9 ❌ (wrong!)
        
        With tracking prev:
        cur = 3, prev = 2
        When we see *3:
        - Undo last addition: 3 - 2 = 1
        - Apply multiplication: 2 * 3 = 6
        - New cur: 1 + 6 = 7 ✓ (correct!)
        
        Formula for multiplication:
        new_cur = cur - prev + (prev * operand)
        
        This handles operator precedence correctly!
        
        Optimizations:
        1. No eval() - track evaluation in O(1)
        2. Build string incrementally
        3. Leading zero check with early break
        4. Only check target at end (not every step)
        
        Time: O(4^n) - still exponential but much faster than TLE
        Space: O(n) - recursion depth
        
        This is INTERVIEW-READY!
        """
        if not num:
            return []

        res = []

        def backtrack(index, path, cur, prev):
            """
            Args:
                index: current position in num
                path: expression string built so far
                cur: current evaluation result
                prev: last term added (for multiplication undo)
            """
            # Base case: used all digits
            if index == len(num):
                if cur == target:
                    res.append(path)
                return

            # Try all possible operand lengths from current position
            for end in range(index + 1, len(num) + 1):
                operand_str = num[index:end]

                # Leading zero guard: "05" or "023" are invalid
                if len(operand_str) > 1 and operand_str[0] == "0":
                    break  # No point trying longer operands

                operand = int(operand_str)

                if index == 0:
                    # First operand - no operator to place
                    # Just start the expression
                    backtrack(end, operand_str, operand, operand)
                else:
                    # Try each operator
                    
                    # Addition: cur + operand
                    # prev = operand (last term is just operand)
                    backtrack(end, path + "+" + operand_str, 
                             cur + operand, operand)

                    # Subtraction: cur - operand
                    # prev = -operand (last term is negative)
                    backtrack(end, path + "-" + operand_str, 
                             cur - operand, -operand)

                    # Multiplication: undo prev, then apply multiplication
                    # Example: "1+2*3"
                    #   After "1+2": cur=3, prev=2
                    #   For "*3": cur - prev + prev*operand = 3 - 2 + 2*3 = 7
                    backtrack(end, path + "*" + operand_str, 
                             cur - prev + prev * operand, prev * operand)

        backtrack(0, "", 0, 0)
        return res


# ==============================================================================
# COMPARISON AND ANALYSIS
# ==============================================================================

"""
SOLUTION 1 (TLE):
✓ Correct logic
✓ Handles leading zeros
✓ Good for understanding the problem
❌ eval() is too slow (parses and evaluates string)
❌ Builds complete strings even for invalid paths
❌ TLE on larger inputs

SOLUTION 2 (Optimal): ⭐
✓ No eval() - tracks evaluation state
✓ O(1) evaluation per step
✓ Handles operator precedence correctly
✓ Early pruning with leading zero break
✓ Clean, elegant code
✓ Interview-ready!

RECOMMENDATION:
Solution 2 is what you should know for interviews!
Shows understanding of:
- Backtracking
- State tracking
- Operator precedence
- Optimization techniques
"""


# ==============================================================================
# KEY INSIGHTS
# ==============================================================================

"""
Why Tracking `prev` is Brilliant:

Problem: Multiplication has higher precedence than +/-
         We can't just multiply current result!

Example: "1+2*3" should be 7, not 9

Wrong approach:
  1 + 2 = 3
  3 * 3 = 9 ❌

Correct with prev tracking:
  After "1+2": cur=3, prev=2
  
  For "*3":
    1. Undo last addition: 3 - 2 = 1
    2. Apply multiplication: 2 * 3 = 6
    3. Add back: 1 + 6 = 7 ✓

Formula:
  new_cur = cur - prev + (prev * operand)
  
This correctly implements operator precedence!

Why each operator needs different prev:
  After "...+5": prev = 5
  After "...-5": prev = -5 (so we can undo subtraction)
  After "...*5": prev = result of multiplication chain
"""


# ==============================================================================
# DETAILED WALKTHROUGH
# ==============================================================================

"""
Example: num = "123", target = 6

Backtracking tree:

Start: index=0, path="", cur=0, prev=0

First operand (no operator yet):
  Try "1": backtrack(1, "1", 1, 1)
    Try "1+2": backtrack(2, "1+2", 3, 2)
      Try "1+2+3": cur=6 ✓ → add "1+2+3"
      Try "1+2*3": cur=3-2+2*3=7 ✗
    Try "1-2": backtrack(2, "1-2", -1, -2)
      Try "1-2+3": cur=2 ✗
      Try "1-2*3": cur=-1-(-2)+(-2)*3=-7 ✗
    Try "1*2": backtrack(2, "1*2", 2, 2)
      Try "1*2+3": cur=5 ✗
      Try "1*2*3": cur=2-2+2*3=6 ✓ → add "1*2*3"
      
  Try "12": backtrack(2, "12", 12, 12)
    Try "12+3": cur=15 ✗
    Try "12-3": cur=9 ✗
    Try "12*3": cur=36 ✗
    
  Try "123": backtrack(3, "123", 123, 123)
    cur=123 ✗

Result: ["1+2+3", "1*2*3"]
"""


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":
    sol = Solution()
    
    test_cases = [
        ("123", 6, ["1*2*3", "1+2+3"]),
        ("232", 8, ["2*3+2", "2+3*2"]),
        ("105", 5, ["1*0+5", "10-5"]),
        ("00", 0, ["0*0", "0+0", "0-0"]),
        ("3456237490", 9191, []),
    ]
    
    print("=" * 70)
    print("TESTING EXPRESSION ADD OPERATORS")
    print("=" * 70)
    print()
    
    for num, target, expected in test_cases:
        result = sol.addOperators(num, target)
        result_set = set(result)
        expected_set = set(expected)
        
        print(f"Input: num = \"{num}\", target = {target}")
        print(f"Output: {result}")
        print(f"Expected: {expected}")
        
        if result_set == expected_set:
            print("✓ PASS")
        else:
            print("✗ FAIL")
            print(f"  Missing: {expected_set - result_set}")
            print(f"  Extra: {result_set - expected_set}")
        print()
    
    print("=" * 70)
    print("WHAT YOU LEARNED:")
    print("=" * 70)
    print()
    print("V1 → V2: From eval() to state tracking")
    print("  - eval() is slow → track evaluation in O(1)")
    print("  - Build strings lazily → faster exploration")
    print("  - Key insight: prev variable for multiplication")
    print()
    print("Why `prev` matters:")
    print("  - Multiplication has higher precedence")
    print("  - Need to undo last term before multiplying")
    print("  - Formula: cur - prev + (prev * operand)")
    print()
    print("This optimization: TLE → AC!")
    print("=" * 70)