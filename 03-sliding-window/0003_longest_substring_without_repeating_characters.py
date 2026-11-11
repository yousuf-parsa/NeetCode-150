"""
LeetCode 3. Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/
Difficulty: Medium

Intuition:
    Checking every substring is too slow.
    So I keep a window [left, right] with no repeats, and a set of its chars.
    When s[right] is already in the set, I shrink from the left until it isn't.
    After each step, the window is valid, so I update the best length.

Complexity:
    Time:  O(n)  - each char enters and leaves the window at most once
    Space: O(k)  - the set (k = number of distinct chars)
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        m = set()
        left = right = 0
        max_len = 0

        while right < len(s):
            while s[right] in m:
                m.remove(s[left])
                left += 1

            max_len = max(max_len, right - left + 1)
            m.add(s[right])
            right += 1

        return max_len


if __name__ == "__main__":
    sol = Solution()
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    assert sol.lengthOfLongestSubstring("pwwkew") == 3
    assert sol.lengthOfLongestSubstring("") == 0
    assert sol.lengthOfLongestSubstring(" ") == 1
    assert sol.lengthOfLongestSubstring("abba") == 2
    print("All tests passed.")
