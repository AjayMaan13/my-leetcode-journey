# 860. Lemonade Change
# https://leetcode.com/problems/lemonade-change/
#
# At a lemonade stand, each lemonade costs $5. Customers pay with $5, $10, or $20 bills.
# You must give correct change to every customer. You start with no change in hand.
# Return true if you can provide every customer with correct change, false otherwise.
#
# Example 1:
#   Input: bills = [5,5,5,10,20]
#   Output: true
#   Explanation: Collect three $5s, then give $5 back for the $10, then give $10+$5 for $20.
#
# Example 2:
#   Input: bills = [5,5,10,10,20]
#   Output: false
#   Explanation: Last customer needs $15 change but we only have two $10 bills.
#
# Constraints:
#   1 <= bills.length <= 10^5
#   bills[i] is either 5, 10, or 20


# Approach 1: Array-based tracking - O(n) time, O(1) space
# Track counts of each denomination in a 3-slot array [count20, count10, count5].
# For each bill, compute required change and greedily give the largest bills first
# ($10 before $5) to preserve the most versatile small bills.
class SolutionArray:
    def lemonadeChange(self, bills):
        inHand = [0, 0, 0]  # [count of $20, $10, $5]

        for bill in bills:
            change = bill - 5  # amount of change we owe

            if change == 0:
                inHand[2] += 1   # $5 bill — just collect it, no change needed

            elif change == 10:   # paid with $10 — give back one $5
                if inHand[2] < 1:
                    return False
                inHand[2] -= 1
                inHand[1] += 1   # collect the $10

            else:                # change == 15, paid with $20 — give back $15
                # prefer $10 + $5 over three $5s (saves $5s for future use)
                if inHand[1] >= 1 and inHand[2] >= 1:
                    inHand[1] -= 1
                    inHand[2] -= 1
                elif inHand[2] >= 3:
                    inHand[2] -= 3
                else:
                    return False
                inHand[0] += 1   # collect the $20

        return True


# Approach 2: Clean variable tracking - O(n) time, O(1) space
# Same greedy logic but with named variables instead of an array — cleaner to read.
# Key greedy insight: when giving $15 change for a $20, prefer $10+$5 over three $5s,
# because $5 bills are the only way to make change for $10 bills too.
class Solution:
    def lemonadeChange(self, bills):
        count5 = count10 = 0

        for bill in bills:
            if bill == 5:
                count5 += 1                    # just collect, no change owed

            elif bill == 10:
                if count5 == 0:
                    return False               # can't make $5 change
                count5 -= 1
                count10 += 1                   # collect the $10

            else:                              # bill == 20, need to give $15 change
                if count10 > 0 and count5 > 0:
                    count10 -= 1               # prefer $10 + $5 (saves $5 bills)
                    count5 -= 1
                elif count5 >= 3:
                    count5 -= 3                # fallback: three $5 bills
                else:
                    return False

        return True


bills = [5, 5, 5, 10, 20]
sol = Solution()
print(sol.lemonadeChange(bills))  # True

bills = [5, 5, 10, 10, 20]
print(sol.lemonadeChange(bills))  # False
