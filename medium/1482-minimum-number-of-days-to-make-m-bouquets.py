"""
1482. Minimum Number of Days to Make m Bouquets
Medium

You are given an integer array bloomDay, an integer m and an integer k.

You want to make m bouquets. To make a bouquet, you need to use k adjacent flowers 
from the garden.

The garden consists of n flowers, the ith flower will bloom in the bloomDay[i] and 
then can be used in exactly one bouquet.

Return the minimum number of days you need to wait to be able to make m bouquets from 
the garden. If it is impossible to make m bouquets return -1.

Example 1:
Input: bloomDay = [1,10,3,10,2], m = 3, k = 1
Output: 3
Explanation: Let us see what happened in the first three days. x means flower bloomed 
and _ means flower did not bloom in the garden.
We need 3 bouquets each should contain 1 flower.
After day 1: [x, _, _, _, _]   // we can only make one bouquet.
After day 2: [x, _, _, _, x]   // we can only make two bouquets.
After day 3: [x, _, x, _, x]   // we can make 3 bouquets. The answer is 3.

Example 2:
Input: bloomDay = [1,10,3,10,2], m = 3, k = 2
Output: -1
Explanation: We need 3 bouquets each has 2 flowers, that means we need 6 flowers. 
We only have 5 flowers so it is impossible to get the needed bouquets and we return -1.

Example 3:
Input: bloomDay = [7,7,7,7,12,7,7], m = 2, k = 3
Output: 12
Explanation: We need 2 bouquets each should have 3 flowers.
Here is the garden after the 7 and 12 days:
After day 7: [x, x, x, x, _, x, x]
We can make one bouquet of the first three flowers that bloomed. We cannot make another 
bouquet from the last three flowers that bloomed because they are not adjacent.
After day 12: [x, x, x, x, x, x, x]
It is obvious that we can make two bouquets in different ways.

Constraints:
- bloomDay.length == n
- 1 <= n <= 10^5
- 1 <= bloomDay[i] <= 10^9
- 1 <= m <= 10^6
- 1 <= k <= n
"""


class Solution(object):
    def minDays_solution1(self, bloomDay, m, k):
        """
        SOLUTION 1: Binary Search on Unique Days
        
        Approach:
        - Binary search on the unique bloom days
        - For each day, check if we can make m bouquets
        
        Issues:
        - Creates sorted list of unique days (extra space and time)
        - Unnecessary conversion: set → list → sort
        - Returns count instead of boolean in helper (less efficient)
        
        Time: O(n log d + d log d) where d = unique days
        - Sort unique days: O(d log d)
        - Binary search: O(log d)
        - Each check: O(n)
        
        Space: O(d) for unique days list
        """
        if len(bloomDay) < m * k:
            return -1
        
        def bouquetsPossible(day):
            """Count number of bouquets we can make by given day"""
            count = 0
            countK = 0
            
            for bloom in bloomDay:
                if bloom <= day:
                    countK += 1
                    if countK == k:
                        count += 1
                        countK = 0
                else:
                    countK = 0
            
            return count
        
        # Create sorted list of unique days
        days = set(bloomDay)
        days = list(days)
        days.sort()
        
        # Binary search on unique days
        low, high = 0, len(days) - 1
        ans = -1
        
        while low <= high:
            mid = (high + low) // 2
            
            if bouquetsPossible(days[mid]) >= m:
                ans = days[mid]
                high = mid - 1
            else:
                low = mid + 1
        
        return ans
    
    def minDays_solution2(self, bloomDay, m, k):
        """
        SOLUTION 2: Binary Search on Range (Optimized!)
        
        Improvements:
        - Binary search directly on range [min(bloomDay), max(bloomDay)]
        - No need to create unique days list
        - Helper returns boolean and exits early when m bouquets found
        - More efficient: stops counting once we have enough bouquets
        
        Approach:
        - low = min(bloomDay), high = max(bloomDay)
        - For each mid day, check if we can make m bouquets
        - If yes, try smaller day (high = mid)
        - If no, need more days (low = mid + 1)
        
        Time: O(n log(max - min))
        - Binary search: O(log(max - min))
        - Each check: O(n) but exits early
        
        Space: O(1)
        
        This is MORE EFFICIENT than Solution 1!
        """
        if len(bloomDay) < m * k:
            return -1
        
        def bouquetsPossible(day):
            """Check if we can make m bouquets by given day"""
            bouquets = 0
            flowers = 0
            
            for bloom in bloomDay:
                if bloom <= day:
                    flowers += 1
                    if flowers == k:
                        bouquets += 1
                        flowers = 0
                        # Early exit: found enough bouquets
                        if bouquets == m:
                            return True
                else:
                    flowers = 0
            
            return False
        
        # Binary search on day range
        low, high = min(bloomDay), max(bloomDay)
        
        while low < high:
            mid = (high + low) // 2
            
            if bouquetsPossible(mid):
                high = mid
            else:
                low = mid + 1
        
        return low
    
    # Main function uses optimized solution
    def minDays(self, bloomDay, m, k):
        """
        :type bloomDay: List[int]
        :type m: int
        :type k: int
        :rtype: int
        """
        return self.minDays_solution2(bloomDay, m, k)