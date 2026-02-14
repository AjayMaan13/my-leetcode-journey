"""
875. Koko Eating Bananas
Medium

Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] 
bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some 
pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, 
she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the 
guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

Example 1:
Input: piles = [3,6,7,11], h = 8
Output: 4

Example 2:
Input: piles = [30,11,23,4,20], h = 5
Output: 30

Example 3:
Input: piles = [30,11,23,4,20], h = 6
Output: 23

Constraints:
- 1 <= piles.length <= 10^4
- piles.length <= h <= 10^9
- 1 <= piles[i] <= 10^9
"""


class Solution(object):
    def minEatingSpeed_original(self, piles, h):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Binary search on eating speed k
        
        Key Insight:
        - Smallest possible k = 1
        - Largest possible k = max(piles)
        - Binary search to find minimum k where hours needed <= h
        
        Time: O(n log m) where n = len(piles), m = max(piles)
        Space: O(1)
        """
        def findH(piles, k):
            """Calculate hours needed for eating speed k"""
            hours = 0
            for pile in piles:
                # Ceiling division: (pile + k - 1) // k
                hours += (pile + k - 1) // k
            return hours
        
        # Binary search on eating speed
        low, high = 1, max(piles)
        
        while low < high:
            mid = (high + low) // 2
            
            # If can finish in time, try smaller speed
            if h >= findH(piles, mid):
                high = mid
            # Need faster speed
            else:
                low = mid + 1
        
        return low
    
    def minEatingSpeed_optimized(self, piles, h):
        """
        OPTIMIZED SOLUTION: Using math.ceil for clarity
        
        Improvements:
        - Use math.ceil for clearer ceiling division
        - Inline helper function for better performance
        - More readable code
        
        Time: O(n log m) where n = len(piles), m = max(piles)
        Space: O(1)
        """
        import math
        
        low, high = 1, max(piles)
        
        while low < high:
            mid = (low + high) // 2
            
            # Calculate hours needed for speed mid
            hours = sum(math.ceil(pile / float(mid)) for pile in piles)
            
            # If can finish in time, try smaller speed
            if hours <= h:
                high = mid
            # Need faster speed
            else:
                low = mid + 1
        
        return low
    
    def minEatingSpeed_alternative(self, piles, h):
        """
        ALTERNATIVE: Using -(-pile // k) for ceiling division
        
        Another way to do ceiling division without importing math
        
        Time: O(n log m)
        Space: O(1)
        """
        low, high = 1, max(piles)
        
        while low < high:
            mid = (low + high) // 2
            
            # Ceiling division using negative floor division
            hours = sum(-(-pile // mid) for pile in piles)
            
            if hours <= h:
                high = mid
            else:
                low = mid + 1
        
        return low
    
    # Main function uses original solution
    def minEatingSpeed(self, piles, h):
        """
        :type piles: List[int]
        :type h: int
        :rtype: int
        """
        return self.minEatingSpeed_original(piles, h)