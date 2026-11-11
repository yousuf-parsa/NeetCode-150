"""
LeetCode 242. Valid Anagram
https://leetcode.com/problems/valid-anagram/
Difficulty: Easy

Intuition:
    Different lengths -> can't be anagrams.
    I count each letter of s in an array of 26 (one slot per letter).
    Then for each letter of t, I subtract 1.
    If any count goes below 0, t has a letter s doesn't have enough of.

Complexity:
    Time:  O(n)  - one pass over each string
    Space: O(1)  - fixed array of 26
"""


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        freq = [0] * 26

        for c in s:
            freq[ord(c) - ord('a')] += 1

        for c in t:
            i = ord(c) - ord('a')
            freq[i] -= 1
            if freq[i] < 0:
                return False
        return True


if __name__ == "__main__":
    sol = Solution()
    assert sol.isAnagram("anagram", "nagaram") is True
    assert sol.isAnagram("rat", "car") is False
    assert sol.isAnagram("a", "ab") is False
    assert sol.isAnagram("aacc", "ccac") is False
    assert sol.isAnagram("", "") is True
    print("All tests passed.")
