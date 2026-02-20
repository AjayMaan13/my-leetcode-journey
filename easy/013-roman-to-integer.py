"""
13. ROMAN TO INTEGER

Problem Statement:
Roman numerals are represented by seven symbols: I, V, X, L, C, D, M

Symbol   Value
I        1
V        5
X        10
L        50
C        100
D        500
M       1000

Roman numerals are usually written largest to smallest from left to right.
However, subtraction is used in six cases:
- I before V (5) or X (10) makes 4 and 9
- X before L (50) or C (100) makes 40 and 90
- C before D (500) or M (1000) makes 400 and 900

Given a roman numeral, convert it to an integer.

Example 1:
Input: s = "III"
Output: 3
Explanation: III = 3

Example 2:
Input: s = "LVIII"
Output: 58
Explanation: L = 50, V = 5, III = 3

Example 3:
Input: s = "MCMXCIV"
Output: 1994
Explanation: M = 1000, CM = 900, XC = 90, IV = 4
"""


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (LOOK BACK WITH CORRECTION)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_LookBack:
    def romanToInt(self, s):
        """
        Track previous character and correct if needed.
        
        Strategy:
        1. Always add current character value
        2. If previous character was smaller, we added it wrong
        3. Correct by subtracting it twice (undo add, then subtract)
        
        Example: "IV"
        - See 'I': add 1, res=1
        - See 'V': prev 'I'(1) < curr 'V'(5)
          → Undo the 1: res = 1 - 1 = 0
          → Add difference: res = 0 + (5-1) = 4 ✓
        
        This works but the correction logic is a bit complex.
        """
        if not s:
            return 0
        
        # Include empty string for initial lastChar
        mapping = {
            "": 0, "I": 1, "V": 5, "X": 10,
            "L": 50, "C": 100, "D": 500, "M": 1000
        }
        
        res = 0
        lastChar = ""  # Track previous character
        
        for ch in s:
            # Check if previous was smaller (subtraction case)
            if mapping[lastChar] < mapping[ch]:
                # We already added lastChar, so remove it
                res -= mapping[lastChar]
                # Then add the correct difference
                res += mapping[ch] - mapping[lastChar]
            else:
                # Normal case: just add current value
                res += mapping[ch]
            
            lastChar = ch  # Update for next iteration
        
        return res


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (LOOK AHEAD - CLEANER)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# This is the STANDARD and CLEANEST solution!

class Solution:
    def romanToInt(self, s):
        """
        Look ahead to next character to decide add or subtract.
        
        Key Insight:
        - If current < next: subtract current (e.g., IV → -1 + 5)
        - Otherwise: add current (normal case)
        
        This is cleaner because:
        - No correction logic needed
        - Decision made immediately
        - More intuitive to explain
        
        Example: "MCMXCIV"
        M(1000): add 1000           → 1000
        C(100) < M(1000): sub 100   → 900
        M(1000): add 1000           → 1900
        X(10) < C(100): sub 10      → 1890
        C(100): add 100             → 1990
        I(1) < V(5): sub 1          → 1989
        V(5): add 5                 → 1994 ✓
        
        This is the RECOMMENDED solution for interviews!
        """
        mapping = {
            "I": 1, "V": 5, "X": 10,
            "L": 50, "C": 100,
            "D": 500, "M": 1000
        }
        
        res = 0
        
        for i in range(len(s)):
            # Look ahead: if current is smaller than next, subtract
            if i + 1 < len(s) and mapping[s[i]] < mapping[s[i + 1]]:
                res -= mapping[s[i]]
            else:
                # Normal case: add current value
                res += mapping[s[i]]
        
        return res


# ==============================================================================
# APPROACH 3: RIGHT TO LEFT (ALTERNATIVE)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)

class Solution_RightToLeft:
    def romanToInt(self, s):
        """
        Process from right to left, tracking last value seen.
        
        Strategy:
        - Start from rightmost (least significant)
        - If current >= last seen: add (normal)
        - If current < last seen: subtract (special case)
        
        Example: "XIV" (14)
        Process right to left:
        - V(5): add 5, last=5 → res=5
        - I(1): 1<5, subtract 1 → res=4
        - X(10): 10>=5, add 10 → res=14 ✓
        
        This is elegant but less intuitive than left-to-right.
        """
        mapping = {
            "I": 1, "V": 5, "X": 10,
            "L": 50, "C": 100,
            "D": 500, "M": 1000
        }
        
        res = 0
        last_value = 0  # Track previous (rightward) value
        
        # Process from right to left
        for i in range(len(s) - 1, -1, -1):
            current = mapping[s[i]]
            
            # If current is smaller than what we've seen, it's subtraction
            if current < last_value:
                res -= current
            else:
                res += current
            
            last_value = current
        
        return res

