"""
1011. Capacity To Ship Packages Within D Days
Medium

A conveyor belt has packages that must be shipped from one port to another within days days.

The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the 
ship with packages on the conveyor belt (in the order given by weights). We may not load 
more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the 
conveyor belt being shipped within days days.

Example 1:
Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
Output: 15
Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

Note that the cargo must be shipped in the order given, so using a ship of capacity 14 
and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is 
not allowed.

Example 2:
Input: weights = [3,2,2,4,1,4], days = 3
Output: 6
Explanation: A ship capacity of 6 is the minimum to ship all the packages in 3 days like this:
1st day: 3, 2
2nd day: 2, 4
3rd day: 1, 4

Example 3:
Input: weights = [1,2,3,1,1], days = 4
Output: 3
Explanation:
1st day: 1
2nd day: 2
3rd day: 3
4th day: 1, 1

Constraints:
- 1 <= days <= weights.length <= 5 * 10^4
- 1 <= weights[i] <= 500
"""


class Solution(object):
    def shipWithinDays_original(self, weights, days):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Binary search on ship capacity
        
        Key Insight:
        - Minimum capacity = max(weights) (must fit largest package)
        - Maximum capacity = sum(weights) (ship everything in 1 day)
        - Binary search to find minimum capacity where days needed <= target days
        
        Issues:
        - Returns high instead of low (should be same but less clear)
        - Extra check "if weightPerDay != 0" is redundant (always true)
        - Could be simplified
        
        Time: O(n log(sum - max))
        Space: O(1)
        
        Works correctly!
        """
        def isdays(weightLimit):
            """Count number of days needed for given weight limit"""
            day = 0
            weightPerDay = 0
            
            for weight in weights:
                weightPerDay += weight
                
                # Exceeds capacity, start new day
                if weightPerDay > weightLimit:
                    day += 1
                    weightPerDay = weight
            
            # Count last day if has packages
            if weightPerDay != 0:
                day += 1
            
            return day
        
        low, high = max(weights), sum(weights)
        
        while low < high:
            mid = (high + low) // 2
            
            if isdays(mid) <= days:
                high = mid
            else:
                low = mid + 1
        
        return high  # Should return low (they're equal at end)
    
    def shipWithinDays_optimized(self, weights, days):
        """
        OPTIMIZED SOLUTION: Cleaner Logic
        
        Improvements:
        - Start with day = 1 (we always need at least 1 day)
        - No need for extra check at end
        - Return low (more standard)
        - Cleaner variable names
        
        Algorithm:
        1. Binary search on capacity range [max(weights), sum(weights)]
        2. For each capacity, simulate loading:
           - Keep adding weights to current day
           - If exceeds capacity, start new day
        3. Find minimum capacity where days needed <= target
        
        Time: O(n log(sum - max))
        Space: O(1)
        """
        def canShip(capacity):
            """Check if can ship all packages within days using given capacity"""
            daysNeeded = 1
            currentLoad = 0
            
            for weight in weights:
                # Try to add package to current day
                if currentLoad + weight > capacity:
                    # Exceeds capacity, need new day
                    daysNeeded += 1
                    currentLoad = weight
                else:
                    currentLoad += weight
            
            return daysNeeded <= days
        
        low, high = max(weights), sum(weights)
        
        while low < high:
            mid = (low + high) // 2
            
            if canShip(mid):
                high = mid
            else:
                low = mid + 1
        
        return low
    
    # Main function uses optimized solution
    def shipWithinDays(self, weights, days):
        """
        :type weights: List[int]
        :type days: int
        :rtype: int
        """
        return self.shipWithinDays_optimized(weights, days)