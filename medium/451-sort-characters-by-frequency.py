"""
451. SORT CHARACTERS BY FREQUENCY

Problem Statement:
Given a string s, sort it in decreasing order based on the frequency of the 
characters. The frequency of a character is the number of times it appears 
in the string.

Return the sorted string. If there are multiple answers, return any of them.

Example 1:
Input: s = "tree"
Output: "eert"
Explanation: 'e' appears twice while 'r' and 't' both appear once.
So 'e' must appear before both 'r' and 't'. Therefore "eetr" is also valid.

Example 2:
Input: s = "cccaaa"
Output: "aaaccc"
Explanation: Both 'c' and 'a' appear three times, so both "cccaaa" and "aaaccc" 
are valid. Note that "cacaca" is incorrect, as same characters must be together.

Example 3:
Input: s = "Aabb"
Output: "bbAa"
Explanation: "bbaA" is also valid, but "Aabb" is incorrect.
Note that 'A' and 'a' are treated as two different characters.
"""

from collections import Counter, defaultdict
import heapq


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (BUCKET SORT - OPTIMAL)
# ==============================================================================
# Time Complexity: O(n) - linear time with bucket sort
# Space Complexity: O(n) - for buckets and result

class Solution_BucketSort:
    def frequencySort(self, s):
        """
        Use bucket sort to sort by frequency in O(n) time.
        
        Key Insight: Frequency range is limited (1 to n), so we can use
        bucket sort instead of comparison-based sorting.
        
        Strategy:
        1. Count frequency of each character
        2. Create buckets where bucket[i] contains chars with frequency i
        3. Iterate buckets from high to low frequency
        4. Build result by repeating each char by its frequency
        
        This is OPTIMAL - O(n) time!
        """
        if not s:
            return ""
        
        res = []
        freqMap = {}  # Maps character -> frequency
        maxFreq = 0   # Track max frequency for bucket array size
        
        # Step 1: Count frequency of each character
        for ch in s:
            freqMap[ch] = 1 + freqMap.get(ch, 0)
            # Track maximum frequency as we go
            if freqMap[ch] > maxFreq:
                maxFreq = freqMap[ch]
        
        # Step 2: Create buckets for each possible frequency
        bucket = []
        for i in range(maxFreq + 1):
            bucket.append([])
        # OR alternative way to create bucket array:
        # bucket = [[] for _ in range(len(s) + 1)]
        # Note: len(s) is safe upper bound since max frequency ≤ len(s)
        
        # Step 3: Place each character into bucket based on its frequency
        # bucket[freq] will contain list of all chars with that frequency
        for ch, freq in freqMap.items():
            bucket[freq].append(ch)
        
        # Step 4: Build result by iterating buckets from high to low
        for i in range(len(bucket) - 1, 0, -1):  # Start from maxFreq down to 1
            for ch in bucket[i]:
                # Repeat character by its frequency and add to result
                # res.append(i * ch)  # Creates Large Temporary Strings - avoid this!
                res.append(ch * i)  # More efficient: string multiplication
        
        return "".join(res)


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (COUNTER + DEFAULTDICT)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n)
#
# Cleaner version using Counter and defaultdict

class Solution_CounterBucket:
    def frequencySort(self, s):
        """
        Use Counter for counting and defaultdict for bucketing.
        
        Improvement over Approach 1:
        - Counter is more Pythonic than manual counting
        - defaultdict automatically initializes empty lists
        - Cleaner, more readable code
        
        Same O(n) time complexity but more elegant.
        """
        if not s:
            return ""
        
        # Step 1: Count frequencies using Counter
        count = Counter(s)  # Maps char -> frequency
        # Example: Counter("tree") -> {'t': 1, 'r': 1, 'e': 2}
        
        # Step 2: Create bucket mapping frequency -> list of characters
        bucket = defaultdict(list)  # Creates a dict that auto-initializes lists
        
        # Step 3: Group characters by their frequency
        for ch, cnt in count.items():
            bucket[cnt].append(ch)
        # Example result: defaultdict(<class 'list'>, {1: ['t', 'r'], 2: ['e']})
        
        # Step 4: Build result from high frequency to low
        res = []
        # Iterate from max possible frequency (len(s)) down to 1
        for i in range(len(s), 0, -1):
            # For each character with this frequency
            for c in bucket[i]:
                # Repeat character by its frequency
                res.append(c * i)
        
        return "".join(res)


# ==============================================================================
# APPROACH 3: YOUR THIRD SOLUTION (SORTING - MOST PYTHONIC)
# ==============================================================================
# Time Complexity: O(n log k) where k is number of unique characters
# Space Complexity: O(n)
#
# One-liner using sorting - most elegant!

class Solution:
    def frequencySort(self, s):
        """
        Count frequencies and sort by frequency using sorted().
        
        Strategy:
        1. Count frequencies with Counter
        2. Sort characters by their frequency (descending)
        3. Build result by repeating each char by its frequency
        
        This is the MOST PYTHONIC solution - elegant one-liner!
        
        Note: O(k log k) sorting where k = unique chars (usually small)
        For most practical inputs, this is very fast and clean.
        """
        # Step 1: Count frequencies
        freq = Counter(s)
        
        # Step 2 & 3: Sort chars by frequency and repeat each char
        # sorted(freq, ...) sorts the keys (characters) of freq dict
        # key=freq.get uses frequency as sort key
        # reverse=True for descending order (highest frequency first)
        return "".join(ch * freq[ch] for ch in sorted(freq, key=freq.get, reverse=True))


# ==============================================================================
# APPROACH 4: HEAP/PRIORITY QUEUE (ALTERNATIVE)
# ==============================================================================
# Time Complexity: O(n log k) where k is unique characters
# Space Complexity: O(n)

class Solution_Heap:
    def frequencySort(self, s):
        """
        Use max heap to get characters in frequency order.
        
        Strategy:
        1. Count frequencies
        2. Push (-freq, char) into heap (negative for max heap)
        3. Pop from heap and build result
        
        This naturally gives us items in frequency order.
        Good alternative to sorting approach.
        """
        if not s:
            return ""
        
        # Count frequencies
        freq = Counter(s)
        
        # Create max heap using negative frequencies
        # Python has min heap, so negate to simulate max heap
        heap = [(-count, char) for char, count in freq.items()]
        heapq.heapify(heap)
        
        # Build result by popping from heap
        res = []
        while heap:
            count, char = heapq.heappop(heap)
            # count is negative, so negate back
            res.append(char * (-count))
        
        return "".join(res)

