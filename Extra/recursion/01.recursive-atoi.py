"""
Recursive Implementation of atoi()

Problem Statement:
    Implement myAtoi(s) which converts a string to a 32-bit signed integer,
    similar to C/C++'s atoi function.

Steps:
    1. Ignore any leading whitespace characters ' '.
    2. Check for an optional sign character '+' or '-'.
       If neither is found, assume positive.
    3. Read digits and build the number. Stop at the first non-digit character
       or end of string. Leading zeros are naturally ignored.
    4. Clamp the result to the 32-bit signed integer range:
         [-2147483648, 2147483647]
       Return INT_MIN if underflow, INT_MAX if overflow.
    5. Return the final integer.

Examples:
    Input : "  -12345"       → Output : -12345
    Input : "4193 with words" → Output : 4193
    Input : "  +42"          → Output : 42
    Input : "words 987"      → Output : 0
    Input : "-91283472332"   → Output : -2147483648  (clamped)
    Input : "2147483648"     → Output :  2147483647  (clamped)
"""

INT_MIN = -(2 ** 31)        # -2147483648
INT_MAX =   2 ** 31 - 1     #  2147483647


# ─────────────────────────────────────────────────────────────────────────────
# RECURSIVE HELPER
# ─────────────────────────────────────────────────────────────────────────────
def helper(s: str, i: int, num: int, sign: int) -> int:
    """
    Recursively reads digits from s starting at index i,
    building up `num` one digit at a time.

    Parameters:
        s    — the input string
        i    — current index we're examining
        num  — accumulated number so far (always positive here; sign applied on return)
        sign — +1 or -1

    Returns:
        The final integer, clamped to [INT_MIN, INT_MAX].
    """
    # ── Base case ─────────────────────────────────────────────────────────────
    # Stop recursing if we've reached the end of the string OR
    # the current character is not a digit (e.g. space, letter, punctuation).
    if i >= len(s) or not s[i].isdigit():
        return sign * num

    # ── Update accumulated number ─────────────────────────────────────────────
    # Shift existing digits left by one decimal place and add the new digit.
    # e.g. num=12, s[i]='3'  →  num = 12*10 + 3 = 123
    num = num * 10 + int(s[i])

    # ── Clamp check (overflow guard) ──────────────────────────────────────────
    # Apply sign temporarily to check against the real bounds.
    # Do this BEFORE the next recursive call so we exit early on overflow.
    if sign * num <= INT_MIN:
        return INT_MIN
    if sign * num >= INT_MAX:
        return INT_MAX

    # ── Recurse on the next character ────────────────────────────────────────
    return helper(s, i + 1, num, sign)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def myAtoi(s: str) -> int:
    """
    Entry point — handles whitespace and sign, then delegates
    digit-reading to the recursive helper.
    """
    i = 0

    # Step 1: skip all leading whitespace
    while i < len(s) and s[i] == ' ':
        i += 1

    # Step 2: determine sign (default positive)
    sign = 1
    if i < len(s) and s[i] in ('+', '-'):
        sign = -1 if s[i] == '-' else 1
        i += 1  # move past the sign character

    # Step 3 → 5: recursive digit parsing + clamping
    return helper(s, i, 0, sign)


# ─────────────────────────────────────────────────────────────────────────────
# Complexity Analysis
#   Time  : O(n) — each character is visited at most once across all
#                  recursive calls (one call per digit character).
#   Space : O(n) — recursive call stack depth is at most n (length of
#                  the digit portion of the string). Not O(1) like an
#                  iterative solution, but acceptable for the problem constraints.
# ─────────────────────────────────────────────────────────────────────────────
