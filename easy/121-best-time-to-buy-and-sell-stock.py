"""
121. Best Time to Buy and Sell Stock

You are given an array prices where prices[i] is the price of a given stock 
on the ith day.

You want to maximize your profit by choosing a single day to buy one stock 
and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. 
If you cannot achieve any profit, return 0.

Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), 
profit = 6-1 = 5.

Example 2:
Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.

Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4
"""

# ============================================================================
# MY SOLUTION - Tracking Difference with Base
# Time: O(n), Space: O(1)
# ============================================================================

def maxProfit_my_solution(prices):
    """
    Track difference from last base price
    Reset base when price drops
    """
    if len(prices) < 1:
        return None
    
    diff = maxDiff = 0
    lastBase = prices[0]
    
    for price in prices[1:]:
        diff = price - lastBase
        if diff < 0:
            lastBase = price  # Found new minimum, update base
            
        maxDiff = max(diff, maxDiff)
        #print(f'price: {price}, diff: {diff}, maxDiff: {maxDiff}')

        
    return maxDiff


# ============================================================================
# SOLUTION 1 - Clean Min Price Tracking (OPTIMAL)
# Time: O(n), Space: O(1)
# ============================================================================

class Solution1:
    def maxProfit(self, prices):
        """
        Track minimum price seen so far and maximum profit
        
        Key Insight:
        - At each day, calculate profit if we sell today
        - Profit = current_price - minimum_price_before_today
        - Keep updating minimum price and maximum profit
        
        Algorithm:
        1. Initialize min_price to infinity, max_profit to 0
        2. For each price:
           - Calculate potential profit (current - min)
           - Update max_profit if this profit is better
           - Update min_price if current price is lower
        """
        min_price = float('inf')
        max_profit = 0
        
        for price in prices:
            # Update minimum price seen so far
            min_price = min(min_price, price)
            # Calculate profit if we sell today
            profit = price - min_price
            # Update maximum profit
            max_profit = max(max_profit, profit)
        
        return max_profit


# ============================================================================
# SOLUTION 2 - Alternative Clean Version
# Time: O(n), Space: O(1)
# ============================================================================

class Solution2:
    def maxProfit(self, prices):
        """
        Same logic, slightly different structure
        More explicit about buy and sell logic
        """
        if not prices:
            return 0
        
        min_price = prices[0]  # Initialize with first price
        max_profit = 0
        
        for price in prices:
            # If we find a lower price, update our buy price
            if price < min_price:
                min_price = price
            # Otherwise, check if selling today gives better profit
            elif price - min_price > max_profit:
                max_profit = price - min_price
        
        return max_profit


# ============================================================================
# SOLUTION 3 - With Buy/Sell Day Tracking
# Time: O(n), Space: O(1)
# ============================================================================

class Solution3:
    def maxProfit(self, prices):
        """
        Same algorithm but also track which days to buy/sell
        """
        min_price = float('inf')
        max_profit = 0
        buy_day = 0
        sell_day = 0
        
        for i, price in enumerate(prices):
            if price < min_price:
                min_price = price
                buy_day = i  # Update potential buy day
            
            profit = price - min_price
            if profit > max_profit:
                max_profit = profit
                sell_day = i  # Update sell day
        
        print(f"Buy on day {buy_day} (price={prices[buy_day]}), "
              f"Sell on day {sell_day} (price={prices[sell_day]})")
        
        return max_profit


# ============================================================================
# VISUAL WALKTHROUGH
# ============================================================================

"""
Example: prices = [7, 1, 5, 3, 6, 4]

Day | Price | min_price | profit (price - min) | max_profit
----|-------|-----------|---------------------|------------
 0  |   7   |     7     |         0           |     0
 1  |   1   |     1     |         0           |     0
 2  |   5   |     1     |         4           |     4
 3  |   3   |     1     |         2           |     4
 4  |   6   |     1     |         5           |     5  ✓
 5  |   4   |     1     |         3           |     5

Final Answer: 5 (Buy at 1, Sell at 6)

Key Pattern:
- Always track the MINIMUM price seen so far
- At each day, calculate: "What if I sell today?"
- Keep the MAXIMUM profit encountered
"""


# ============================================================================
# COMPARISON WITH KADANE'S ALGORITHM
# ============================================================================

"""
Similarities:
- Both are single-pass O(n) algorithms
- Both track a running value and a maximum

Key Differences:

Kadane's (Max Subarray):
- Tracks: running sum
- Resets: when sum becomes negative
- Calculates: sum of elements

Stock Problem:
- Tracks: minimum price
- Updates: when price is lower
- Calculates: difference (price - min)

Why Kadane's doesn't work directly:
- Kadane's adds/subtracts elements (sum-based)
- Stock needs price difference (not cumulative)
- Stock must maintain buy < sell constraint
"""


# ============================================================================
# COMPLEXITY COMPARISON
# ============================================================================

"""
Approach                    Time        Space       Notes
--------                    ----        -----       -----
My Solution                 O(n)        O(1)        Works! Good logic
Min Price Tracking          O(n)        O(1)        Cleaner variable names
With Buy/Sell Days          O(n)        O(1)        Extra tracking

All solutions are optimal! Your solution is correct.
The "official" solutions just have cleaner variable naming.
"""


