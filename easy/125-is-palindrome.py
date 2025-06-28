"""
LeetCode 125 — Valid Palindrome
Difficulty: Easy

📝 Problem Statement:
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters
and removing all non-alphanumeric characters, it reads the same forward and backward.

Alphanumeric characters include letters and numbers.

Given a string s, return True if it is a palindrome, or False otherwise.

---

🔸 Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: True
Explanation:
After removing non-alphanumeric characters and converting to lowercase,
"s" becomes "amanaplanacanalpanama", which is a palindrome.

🔸 Example 2:
Input: s = "race a car"
Output: False
Explanation:
After cleaning, "raceacar" is not a palindrome.

🔸 Example 3:
Input: s = " "
Output: True
Explanation:
An empty string after removing non-alphanumeric characters is considered a palindrome.

---

🔧 Constraints:
- 1 <= s.length <= 2 * 10^5
- s consists only of printable ASCII characters.

---

💡 Follow-up:
- Could you solve it without using extra space?
"""

class Solution(object):
    def isPalindrome(self, s):

        left, right = 0, len(s) - 1

        while left < right:
            while left < right and not s[left].isalnum(): 
                left += 1
            while left < right and not s[right].isalnum(): 
                right -= 1

            if s[left].lower() != s[right].lower(): 
                return False
            left += 1
            right -= 1
        return True


# Example usage:
if __name__ == "__main__":
    sol = Solution()
    test_cases = [
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
    ]
    for s, expected in test_cases:
        result = sol.isPalindrome(s)
        print(f'isPalindrome("{s}") = {result} (Expected: {expected})')
