"""
8. STRING TO INTEGER (ATOI)

Problem Statement:
Implement myAtoi(string s) which converts a string to a 32-bit signed integer.

Algorithm:
1. Whitespace: Ignore any leading whitespace
2. Signedness: Determine sign by checking for '-' or '+', assume positive if neither
3. Conversion: Read integer by skipping leading zeros until non-digit or end
4. Rounding: Clamp to 32-bit signed integer range [-2^31, 2^31 - 1]

Example 1:
Input: s = "42"
Output: 42

Example 2:
Input: s = " -042"
Output: -42

Example 3:
Input: s = "1337c0d3"
Output: 1337

Example 4:
Input: s = "0-1"
Output: 0

Example 5:
Input: s = "words and 987"
Output: 0
"""


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (STRING BUILDING WITH FLAGS)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n) - storing digits in list

class Solution_StringBuilding:
    def myAtoi(self, s):
        """
        Build number as string, then convert at the end.
        
        Strategy:
        1. Use flags to track state (negative, positive, int started)
        2. Collect digits in a list
        3. Convert to integer at the end
        4. Clamp to 32-bit range
        
        This works but has complex flag logic and edge cases.
        """
        def valueExceeded(res):
            """Clamp value to 32-bit signed integer range"""
            if res > 2147483647:  # 2^31 - 1
                return 2147483647
            elif res < -2147483648:  # -2^31
                return -2147483648
            else:
                return res
        
        def returnValue(res):
            """Convert collected digits to final integer"""
            if res:
                # Join digits and convert to int, apply sign
                num = int("".join(res))
                if negativeOn:
                    num *= -1
                return valueExceeded(num)
            else:
                return 0
        
        if not s:
            return 0
        
        res = []  # Collect digit characters
        integers = "0123456789"
        negativeOn = False
        positiveOn = False
        intStarted = False
        
        for ch in s:
            # Skip leading whitespace (only before digits/sign)
            if (ch == " ") and not res and not negativeOn and not positiveOn:
                continue
            
            # Handle positive sign (only before digits)
            elif ch == "+" and not res and not negativeOn and not positiveOn:
                positiveOn = True
            
            # Collect digits
            elif ch in integers:
                intStarted = True
                res.append(ch)
            
            # Handle negative sign (only before digits, no + seen)
            elif ch == "-" and not negativeOn and not intStarted and not positiveOn:
                negativeOn = True
            
            # Any other character stops parsing
            else:
                return returnValue(res)
        
        return returnValue(res)


# ==============================================================================
# APPROACH 2: STATE MACHINE (CLEANER - OPTIMAL)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1) - only storing integer result

class Solution:
    def myAtoi(self, s):
        """
        State machine approach - cleaner and more efficient.
        
        Strategy:
        1. Strip leading whitespace with lstrip()
        2. Check for sign character
        3. Parse digits one by one, building number incrementally
        4. Check for overflow BEFORE multiplying by 10
        
        This is the OPTIMAL solution:
        - No string building (O(1) space for number)
        - Clear state transitions
        - Overflow check during parsing (more efficient)
        """
        # Remove leading whitespace
        s = s.lstrip()
        
        # Empty string check
        if not s:
            return 0
        
        # Initialize parsing state
        i = 0
        sign = 1
        
        # Handle sign character
        if s[i] == "+":
            i += 1
        elif s[i] == "-":
            i += 1
            sign = -1
        
        # Parse digits
        parsed = 0
        
        while i < len(s):
            cur = s[i]
            
            # Stop if non-digit character
            if not cur.isdigit():
                break
            else:
                # Build number: shift left and add new digit
                parsed = parsed * 10 + int(cur)
            
            i += 1
        
        # Apply sign
        parsed *= sign
        
        # Clamp to 32-bit signed integer range
        if parsed > 2**31 - 1:
            return 2**31 - 1
        elif parsed < -2**31:
            return -2**31
        else:
            return parsed


# ==============================================================================
# APPROACH 3: OVERFLOW CHECK DURING PARSING (MOST OPTIMAL)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
#
# Checks overflow BEFORE multiplication to avoid integer overflow

class Solution_OverflowCheck:
    def myAtoi(self, s):
        """
        Check for overflow BEFORE multiplying to avoid edge cases.
        
        Key improvement: Check if result will overflow before doing math.
        This prevents potential issues with very large intermediate values.
        
        Formula: if result > (INT_MAX - digit) // 10, overflow will occur
        
        This is the PRODUCTION-READY solution.
        """
        i = 0
        n = len(s)
        sign = 1
        result = 0
        
        # Define 32-bit integer bounds
        INT_MAX = 2**31 - 1  # 2147483647
        INT_MIN = -2**31     # -2147483648
        
        # Step 1: Skip whitespace
        while i < n and s[i] == ' ':
            i += 1
        
        # Step 2: Handle sign
        if i < n and (s[i] == '+' or s[i] == '-'):
            sign = -1 if s[i] == '-' else 1
            i += 1
        
        # Step 3: Convert digits
        while i < n and s[i].isdigit():
            digit = int(s[i])
            
            # Step 4: Check overflow BEFORE multiplying
            # If result > (INT_MAX - digit) // 10, then result * 10 + digit > INT_MAX
            if result > (INT_MAX - digit) // 10:
                return INT_MAX if sign == 1 else INT_MIN
            
            result = result * 10 + digit
            i += 1
        
        return sign * result


# ==============================================================================
# APPROACH 4: REGEX (PYTHONIC BUT OVERKILL)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n)

import re

class Solution_Regex:
    def myAtoi(self, s):
        """
        Use regex to extract the number pattern.
        
        Pattern: optional whitespace + optional sign + digits
        
        This is clever but overkill for interviews.
        Good to know but not recommended as primary solution.
        """
        s = s.lstrip()  # Remove leading whitespace
        
        # Match optional sign followed by digits
        match = re.match(r'^[+-]?\d+', s)
        
        if not match:
            return 0
        
        # Convert matched string to integer
        result = int(match.group())
        
        # Clamp to 32-bit range
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31
        
        if result > INT_MAX:
            return INT_MAX
        elif result < INT_MIN:
            return INT_MIN
        else:
            return result
