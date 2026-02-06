"""
18. 4Sum
Medium

Given an array nums of n integers, return an array of all the unique quadruplets 
[nums[a], nums[b], nums[c], nums[d]] such that:
- 0 <= a, b, c, d < n
- a, b, c, and d are distinct.
- nums[a] + nums[b] + nums[c] + nums[d] == target

You may return the answer in any order.

Example 1:
Input: nums = [1,0,-1,0,-2,2], target = 0
Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]

Example 2:
Input: nums = [2,2,2,2,2], target = 8
Output: [[2,2,2,2]]

Constraints:
- 1 <= nums.length <= 200
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
"""


class Solution(object):
    def fourSum_original(self, nums, target):
        """
        ORIGINAL SOLUTION (Your Approach)
        
        Approach: Two nested loops + Two pointers
        
        Issues:
        1. Duplicate check for j is incorrect:
           - if j > i + 1 and (nums[j] == nums[j - 1] or nums[i] == nums[j])
           - The condition "nums[i] == nums[j]" is wrong
           - It prevents valid quadruplets like [2,2,2,2]
        2. Only skips duplicates for left pointer, not right pointer
        3. Condition should be: if j > i + 1 and nums[j] == nums[j - 1]
        
        Time Complexity: O(n³)
        Space Complexity: O(1) excluding output
        
        Pros:
        - Basic structure is correct
        - Uses two-pointer technique
        
        Cons:
        - Wrong duplicate check causes missed solutions
        - Doesn't skip duplicates for right pointer
        """
        if len(nums) < 4:
            return []
        
        res = []
        n = len(nums)
        nums.sort()

        for i in range(n):
            # Skip duplicate for i
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            for j in range(i + 1, n):
                # ❌ WRONG: nums[i] == nums[j] prevents valid cases
                if j > i + 1 and (nums[j] == nums[j - 1] or nums[i] == nums[j]):
                    continue
                
                left = j + 1
                right = n - 1
                
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]
                    
                    if total > target:
                        right -= 1
                    elif total < target:
                        left += 1
                    else:
                        res.append([nums[i], nums[j], nums[left], nums[right]])
                        left += 1
                        
                        # Skip duplicates for left
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
        
        return res
    
    def fourSum_optimized(self, nums, target):
        """
        OPTIMIZED SOLUTION (Fixed Version)
        
        Improvements:
        1. Fixed duplicate check for j: only check nums[j] == nums[j-1]
        2. Added duplicate skip for right pointer
        3. Clearer variable names
        
        Algorithm:
        1. Sort array
        2. Two outer loops for first two elements
        3. Two pointers for remaining two elements
        4. Skip duplicates at each level
        
        Time Complexity: O(n³)
        - Two nested loops: O(n²)
        - Two pointers: O(n) per iteration
        - Total: O(n³)
        
        Space Complexity: O(1) excluding output
        
        ⭐⭐ Good solution for 4Sum specifically
        """
        if len(nums) < 4:
            return []
        
        res = []
        nums.sort()
        n = len(nums)
        
        for i in range(n - 3):  # Need at least 4 elements after i
            # Skip duplicate for first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            for j in range(i + 1, n - 2):  # Need at least 2 elements after j
                # Skip duplicate for second element
                # ✅ FIXED: Only check nums[j] == nums[j-1]
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue
                
                # Two pointers for remaining elements
                left = j + 1
                right = n - 1
                
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]
                    
                    if total < target:
                        left += 1
                    elif total > target:
                        right -= 1
                    else:
                        # Found valid quadruplet
                        res.append([nums[i], nums[j], nums[left], nums[right]])
                        
                        # Skip duplicates for left
                        left += 1
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        
                        # Skip duplicates for right
                        right -= 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
        
        return res
    
    def fourSum_kSum_recursive(self, nums, target):
        """
        APPROACH 3: Recursive kSum (From Screenshot - MOST ELEGANT!) ⭐⭐⭐
        
        Key Insight:
        - 4Sum is just a special case of kSum
        - Can be solved recursively:
          - kSum reduces to (k-1)Sum
          - Base case: k=2 (two pointers)
        
        This approach generalizes to ANY k-Sum problem!
        
        Algorithm:
        1. Sort array once
        2. kSum(k=4, start=0, target)
        3. Recursively reduce k until k=2
        4. Base case: Use two pointers
        
        Benefits:
        - Generalizes to 3Sum, 4Sum, 5Sum, etc.
        - Clean recursive structure
        - Handles duplicates elegantly
        - Reusable code
        
        Time Complexity: O(n^(k-1)) where k=4
        - For 4Sum: O(n³)
        
        Space Complexity: O(k) for recursion stack
        
        ⭐⭐⭐ BEST SOLUTION: Elegant and generalizable!
        """
        nums.sort()
        res = []
        
        def kSum(k, start, target):
            """
            Recursive helper to find k numbers that sum to target
            
            Parameters:
            - k: number of elements to find
            - start: starting index in nums
            - target: target sum
            
            Returns when:
            - k == 2: Use two pointers (base case)
            - k > 2: Recursively find (k-1) elements
            """
            # Base case: Two Sum using two pointers
            if k == 2:
                # Two pointers approach
                l, r = start, len(nums) - 1
                
                while l < r:
                    current_sum = nums[l] + nums[r]
                    
                    if current_sum < target:
                        l += 1
                    elif current_sum > target:
                        r -= 1
                    else:
                        # Found valid pair, add to result
                        res.append(quad + [nums[l], nums[r]])
                        l += 1
                        
                        # Skip duplicates for left pointer
                        while l < r and nums[l] == nums[l - 1]:
                            l += 1
                return
            
            # Recursive case: Fix one element, find (k-1) elements
            for i in range(start, len(nums) - k + 1):
                # Skip duplicates for current element
                if i > start and nums[i] == nums[i - 1]:
                    continue
                
                # Add current element to quad (building quadruplet)
                quad.append(nums[i])
                
                # Recursively find (k-1) elements that sum to (target - nums[i])
                kSum(k - 1, i + 1, target - nums[i])
                
                # Backtrack: remove current element
                quad.pop()
        
        # Start with empty quadruplet
        quad = []
        # Find 4 elements starting from index 0 that sum to target
        kSum(4, 0, target)
        
        return res
    
    def fourSum_kSum_with_comments(self, nums, target):
        """
        SAME AS RECURSIVE kSum but with DETAILED COMMENTS for understanding
        """
        nums.sort()  # Sort once at the beginning
        res = []     # Store all valid quadruplets
        quad = []    # Current quadruplet being built
        
        def kSum(k, start, target):
            """
            Find k numbers starting from index 'start' that sum to 'target'
            
            How it works:
            - When k=4: Find 4 numbers
            - When k=3: Find 3 numbers
            - When k=2: Use two pointers (base case)
            """
            
            # BASE CASE: When we need to find 2 numbers (Two Sum II)
            if k == 2:
                l, r = start, len(nums) - 1
                
                while l < r:
                    current_sum = nums[l] + nums[r]
                    
                    if current_sum < target:
                        # Sum too small, need larger number
                        l += 1
                    elif current_sum > target:
                        # Sum too large, need smaller number
                        r -= 1
                    else:
                        # Perfect! Found valid pair
                        # quad already has (k-2) elements
                        # Add these 2 elements to complete quadruplet
                        res.append(quad + [nums[l], nums[r]])
                        l += 1
                        
                        # Skip duplicate values for left pointer
                        while l < r and nums[l] == nums[l - 1]:
                            l += 1
                return
            
            # RECURSIVE CASE: When we need to find k > 2 numbers
            # Strategy: Fix one element, find (k-1) elements
            
            # Loop through possible first elements
            # Stop at len(nums) - k + 1 to ensure enough elements remain
            for i in range(start, len(nums) - k + 1):
                # Skip duplicate values to avoid duplicate quadruplets
                # Only skip if not the first element we're considering
                if i > start and nums[i] == nums[i - 1]:
                    continue
                
                # Choose nums[i] as one of our k elements
                quad.append(nums[i])
                
                # Recursively find (k-1) elements from remaining array
                # New target: (target - nums[i])
                # Start searching from: i + 1
                kSum(k - 1, i + 1, target - nums[i])
                
                # Backtrack: remove nums[i] to try next element
                quad.pop()
        
        # Initial call: Find 4 elements starting from index 0
        kSum(4, 0, target)
        return res
    
    # Main function uses recursive kSum (most elegant)
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        return self.fourSum_kSum_recursive(nums, target)


"""
============================================================================
DETAILED EXPLANATION: Recursive kSum Approach
============================================================================

Visual Example: nums = [1,0,-1,0,-2,2], target = 0

Step 1: Sort array
------
nums = [-2, -1, 0, 0, 1, 2]

Step 2: Call kSum(4, 0, 0)
------
Looking for 4 numbers starting at index 0 that sum to 0

Iteration 1: i=0, nums[0]=-2
  quad = [-2]
  Call kSum(3, 1, 2)  ← Find 3 numbers that sum to 2
  
    Iteration 1: i=1, nums[1]=-1
      quad = [-2, -1]
      Call kSum(2, 2, 3)  ← Find 2 numbers that sum to 3
      
        Two pointers: l=2, r=5
        nums[2]=0, nums[5]=2 → sum=2 (too small)
        l=3, r=5
        nums[3]=0, nums[5]=2 → sum=2 (too small)
        l=4, r=5
        nums[4]=1, nums[5]=2 → sum=3 ✓
        res.append([-2, -1, 1, 2])
      
      quad.pop() → quad = [-2]
    
    Iteration 2: i=2, nums[2]=0
      quad = [-2, 0]
      Call kSum(2, 3, 2)  ← Find 2 numbers that sum to 2
      
        Two pointers: l=3, r=5
        nums[3]=0, nums[5]=2 → sum=2 ✓
        res.append([-2, 0, 0, 2])
      
      quad.pop() → quad = [-2]
  
  quad.pop() → quad = []

Iteration 2: i=1, nums[1]=-1
  quad = [-1]
  Call kSum(3, 2, 1)  ← Find 3 numbers that sum to 1
  
    ... similar process ...
    res.append([-1, 0, 0, 1])

Final result: [[-2,-1,1,2], [-2,0,0,2], [-1,0,0,1]]


============================================================================
WHY RECURSIVE kSum IS BETTER
============================================================================

Traditional 4Sum (Nested Loops):
---------------------------------
for i in range(n):
    for j in range(i+1, n):
        for left/right pointers...

Problems:
❌ Code duplication for 3Sum, 4Sum, 5Sum
❌ Hard to extend to kSum
❌ Lots of repetitive duplicate-skipping logic


Recursive kSum:
---------------
def kSum(k, start, target):
    if k == 2: two_pointers()
    else: recurse with k-1

Benefits:
✅ ONE solution works for ANY k
✅ Clean recursive structure
✅ Easy to understand
✅ Duplicate handling in one place
✅ Can solve 3Sum, 4Sum, 5Sum with same code!


============================================================================
COMPARISON OF ALL APPROACHES
============================================================================

Approach 1: Original (Your Code)
---------------------------------
Time: O(n³)
Space: O(1)
Issues: Wrong duplicate check
Rating: ⭐ (Has bugs)


Approach 2: Optimized (Fixed Loops)
------------------------------------
Time: O(n³)
Space: O(1)
Improvements: Fixed duplicate checks
Rating: ⭐⭐ (Works but not elegant)


Approach 3: Recursive kSum (Screenshot)
----------------------------------------
Time: O(n³)
Space: O(k) = O(4) = O(1)
Benefits:
  - Generalizes to any k
  - Cleaner code
  - Reusable
  - Better design pattern
Rating: ⭐⭐⭐ (Best approach!)


============================================================================
HOW TO USE kSum FOR OTHER PROBLEMS
============================================================================

For 3Sum (k=3):
---------------
kSum(3, 0, 0)  # Find 3 numbers that sum to 0


For 5Sum (k=5):
---------------
kSum(5, 0, target)  # Find 5 numbers that sum to target


For kSum with k=anything:
-------------------------
kSum(k, 0, target)  # Find k numbers that sum to target


The recursive kSum is a DESIGN PATTERN you can use for:
- 3Sum, 4Sum, 5Sum, ..., kSum
- Any "find k elements that satisfy condition" problem


============================================================================
KEY TAKEAWAYS
============================================================================

1. Your original solution has a bug:
   ❌ "nums[i] == nums[j]" prevents valid cases like [2,2,2,2]
   ✅ Should only check "nums[j] == nums[j-1]"

2. The recursive kSum approach is BEST because:
   ✅ Works for any k (3Sum, 4Sum, 5Sum, ...)
   ✅ Clean and elegant
   ✅ Easy to understand
   ✅ Production-quality code

3. Pattern Recognition:
   - kSum reduces to (k-1)Sum
   - Base case: k=2 (Two Pointers)
   - This is a classic "reduce problem size" recursion

4. Interview Tip:
   If asked for 4Sum, mention the kSum generalization
   Shows advanced thinking and design skills!
"""