"""
205. ISOMORPHIC STRINGS

Problem Statement:
Given two strings s and t, determine if they are isomorphic.

Two strings s and t are isomorphic if the characters in s can be replaced to 
get t. All occurrences of a character must be replaced with another character 
while preserving the order of characters. No two characters may map to the 
same character, but a character may map to itself.

Example 1:
Input: s = "egg", t = "add"
Output: true
Explanation: 'e' → 'a', 'g' → 'd'

Example 2:
Input: s = "foo", t = "bar"
Output: false
Explanation: 'o' cannot map to both 'a' and 'r'

Example 3:
Input: s = "paper", t = "title"
Output: true
Explanation: 'p'→'t', 'a'→'i', 'e'→'l', 'r'→'e'

Note: The mapping must be bidirectional - no two characters can map to the same character.
"""


# ==============================================================================
# APPROACH 1: YOUR FIRST SOLUTION (TWO HASH MAPS - OPTIMAL)
# ==============================================================================
# Time Complexity: O(n) where n is length of string
# Space Complexity: O(1) - at most 256 characters (constant space)

class Solution_TwoMaps:
    def isIsomorphic(self, s, t):
        """
        Use two hash maps to track bidirectional mapping.
        
        Strategy:
        1. Maintain s_to_t mapping (s[i] → t[i])
        2. Maintain t_to_s mapping (t[i] → s[i])
        3. For each character pair:
           - If s[i] already mapped, verify it maps to t[i]
           - If t[i] already mapped, verify it maps to s[i]
           - Otherwise, create both mappings
        
        Why two maps?
        - s_to_t ensures each char in s maps to only one char in t
        - t_to_s ensures no two chars in s map to same char in t
        - Both conditions are necessary for isomorphism
        
        This is the OPTIMAL solution - clean and efficient.
        """
        if not s or not t or len(s) != len(t):
            return False

        s_to_t = {}  # Maps characters from s to t
        t_to_s = {}  # Maps characters from t to s

        for i in range(len(s)):
            char_s = s[i]
            char_t = t[i]
            
            # Check if s[i] already has a mapping
            if char_s in s_to_t:
                # Verify it maps to current t[i]
                if t[i] != s_to_t[char_s]:
                    return False
            
            # Check if t[i] already has a reverse mapping
            elif char_t in t_to_s:
                # Verify it maps to current s[i]
                if s[i] != t_to_s[char_t]:
                    return False
            
            # No existing mappings - create new ones
            else:
                s_to_t[char_s] = char_t
                t_to_s[char_t] = char_s

        return True


# ==============================================================================
# APPROACH 2: YOUR SECOND SOLUTION (ONE MAP + VALUES CHECK)
# ==============================================================================
# Time Complexity: O(n²) - values() check is O(n) per iteration
# Space Complexity: O(1)
#
# Works but less efficient due to values() lookup

class Solution_OneMapWithValues:
    def isIsomorphic(self, s, t):
        """
        Use one map but check if value already exists.
        
        Strategy:
        1. Maintain only s_to_t mapping
        2. When adding new mapping, check if t[i] already in values
        
        Why less efficient?
        - mapping.values() creates a view and checking membership is O(n)
        - This makes overall complexity O(n²)
        - Still correct, just slower than two-map approach
        
        Trade-off: Slightly less space but worse time complexity.
        """
        if len(s) != len(t):
            return False
        
        mapping = {}
        
        for i in range(len(s)):
            c1 = s[i]
            c2 = t[i]
            
            # Check if character already has a mapping
            if c1 in mapping:
                if mapping[c1] != c2:
                    return False
            else:
                # Check if c2 is already mapped to by another character
                # This is O(n) operation!
                if c2 in mapping.values():
                    return False
                mapping[c1] = c2
        
        return True


# ==============================================================================
# APPROACH 3: TRANSFORMATION PATTERN (OPTIMAL ALTERNATIVE)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n)
#
# Different approach: Compare transformation patterns

class Solution:
    def isIsomorphic(self, s, t):
        """
        Compare transformation patterns of both strings.
        
        Key Insight: Two strings are isomorphic if they have the same pattern.
        We can represent pattern by first occurrence indices.
        
        Strategy:
        1. For each string, map each character to its first occurrence index
        2. If both strings produce same pattern list, they're isomorphic
        
        Example:
        s = "egg" → pattern: [0, 1, 1]
        t = "add" → pattern: [0, 1, 1]
        Patterns match → isomorphic!
        
        s = "foo" → pattern: [0, 1, 1]
        t = "bar" → pattern: [0, 1, 2]
        Patterns differ → not isomorphic!
        
        This elegantly handles bidirectional mapping in one pass.
        """
        def get_pattern(string):
            """
            Map each character to index of its first occurrence.
            Returns list of first occurrence indices.
            """
            char_to_index = {}
            pattern = []
            
            for i, char in enumerate(string):
                if char not in char_to_index:
                    char_to_index[char] = i
                pattern.append(char_to_index[char])
            
            return pattern
        
        # Compare patterns of both strings
        return get_pattern(s) == get_pattern(t)


# ==============================================================================
# APPROACH 4: ONE-LINER WITH ZIP AND SET (PYTHONIC)
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(n)

class Solution_OneLiner:
    def isIsomorphic(self, s, t):
        """
        Clever one-liner using zip and set properties.
        
        Key insight:
        - len(set(zip(s, t))): Number of unique (s[i], t[i]) pairs
        - len(set(s)): Number of unique chars in s
        - len(set(t)): Number of unique chars in t
        
        For isomorphism:
        - Each char in s maps to exactly one char in t: len(pairs) = len(set(s))
        - Each char in t maps from exactly one char in s: len(pairs) = len(set(t))
        
        If all three are equal, strings are isomorphic!
        
        Example:
        s = "egg", t = "add"
        pairs: {('e','a'), ('g','d')} → len = 2
        set(s): {'e', 'g'} → len = 2
        set(t): {'a', 'd'} → len = 2
        All equal → isomorphic!
        """
        return len(set(zip(s, t))) == len(set(s)) == len(set(t))

