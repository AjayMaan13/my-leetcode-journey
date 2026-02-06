"""
15. 3Sum
Medium

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] 
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Example 1:
Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

Example 2:
Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.

Example 3:
Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.

Constraints:
- 3 <= nums.length <= 3000
- -10^5 <= nums[i] <= 10^5
"""


class Solution(object):
    def threeSum_original(self, nums):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Sort + Two Pointers for each element
        
        Issues:
        1. Unnecessary check: if len(nums) < 3 (constraints guarantee >= 3)
        2. Returns None instead of []
        3. Inefficient duplicate check: [nums[i], nums[left], nums[right]] not in res
           - This is O(n) operation for each triplet found!
           - With list comparison, this becomes very slow
        4. No skipping of duplicate elements
           - Example: [-1,-1,2] can be found multiple times
        
        Time Complexity: O(n³) worst case
        - Sorting: O(n log n)
        - Outer loop: O(n)
        - Two pointers: O(n)
        - Checking "not in res": O(n) per triplet
        - Total: O(n² × n) = O(n³) due to duplicate check
        
        Space Complexity: O(n) for result storage
        
        Pros:
        - Basic logic is correct
        - Uses two-pointer technique
        
        Cons:
        - Very slow due to "not in res" check
        - Doesn't skip duplicates intelligently
        - Will TLE (Time Limit Exceeded) on large inputs
        """
        if len(nums) < 3:
            return  # Returns None
        
        res = []
        n = len(nums)
        nums.sort()
        
        for i in range(n):
            left = i + 1
            right = n - 1
            
            while left < right:
                if nums[left] + nums[right] > -nums[i]:
                    right -= 1
                elif nums[left] + nums[right] < -nums[i]:
                    left += 1
                else:
                    # ❌ This check is O(n) and causes TLE(Time Limit Exceeded!
                    if [nums[i], nums[left], nums[right]] not in res:
                        res.append([nums[i], nums[left], nums[right]])
                    left += 1 
                    right -= 1
        
        return res
    
    def threeSum_optimized(self, nums):
        """
        OPTIMIZED SOLUTION (From Screenshot - BEST!)
        
        Key Improvements:
        1. Skip duplicate elements for 'i' using: if i > 0 and a == nums[i-1]: continue
        2. Skip duplicate elements for 'l' and 'r' using while loops
        3. No need for "not in res" check - duplicates handled at source!
        
        Algorithm:
        1. Sort array
        2. For each element 'a' at index i:
           a. Skip if same as previous (avoid duplicate triplets)
           b. Use two pointers (l, r) to find pairs that sum to -a
           c. When found:
              - Add triplet to result
              - Skip all duplicate values for l
              - Move both pointers inward
        
        Why This is Better:
        - Handles duplicates DURING iteration, not after
        - No expensive "not in res" check
        - Clean and efficient
        
        Time Complexity: O(n²)
        - Sorting: O(n log n)
        - Outer loop: O(n)
        - Two pointers: O(n) per iteration
        - Total: O(n²)
        
        Space Complexity: O(1) excluding output array
        
        ⭐⭐⭐ OPTIMAL SOLUTION!
        """
        res = []
        nums.sort()
        
        for i, a in enumerate(nums):
            # Skip duplicate values for 'a'
            # This prevents finding duplicate triplets
            if i > 0 and a == nums[i - 1]:
                continue
            
            # Two pointers approach
            l, r = i + 1, len(nums) - 1
            
            while l < r:
                threeSum = a + nums[l] + nums[r]
                
                if threeSum > 0:
                    r -= 1  # Sum too large, decrease right pointer
                elif threeSum < 0:
                    l += 1  # Sum too small, increase left pointer
                else:
                    # Found a valid triplet
                    res.append([a, nums[l], nums[r]])
                    l += 1
                    
                    # Skip duplicate values for 'l'
                    # This ensures we don't add duplicate triplets
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1
            
        return res
    
    def threeSum_with_comments(self, nums):
        """
        SAME AS OPTIMIZED but with detailed comments for learning
        """
        res = []
        nums.sort()  # Sort to enable two-pointer technique and handle duplicates
        
        for i, a in enumerate(nums):
            # Duplicate Check for First Element:
            # If current element equals previous, skip it
            # Example: [-1, -1, 0, 1] → Process first -1, skip second -1
            if i > 0 and a == nums[i - 1]:
                continue
            
            # Set up two pointers
            l = i + 1        # Left pointer starts after current element
            r = len(nums) - 1  # Right pointer starts at end
            
            while l < r:
                threeSum = a + nums[l] + nums[r]
                
                if threeSum > 0:
                    # Sum too large, need smaller number
                    # Move right pointer left (to smaller values)
                    r -= 1
                    
                elif threeSum < 0:
                    # Sum too small, need larger number
                    # Move left pointer right (to larger values)
                    l += 1
                    
                else:
                    # Found valid triplet! Sum equals 0
                    res.append([a, nums[l], nums[r]])
                    l += 1  # Move left pointer to continue searching
                    
                    # Duplicate Check for Second Element:
                    # Skip all duplicate values of nums[l]
                    # Example: [-1, 0, 0, 0, 1] → Use first 0, skip rest
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1
        
        return res
    
    # Main function uses optimized approach
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        return self.threeSum_optimized(nums)

