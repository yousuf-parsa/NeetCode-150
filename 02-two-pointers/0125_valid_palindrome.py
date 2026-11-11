"""
LeetCode 125. Valid Palindrome
https://leetcode.com/problems/valid-palindrome/
Difficulty: Easy

Intuition:
    I compare from both ends with two pointers: left and right.
    Each pointer skips anything that isn't a letter or digit.
    Then I compare the two chars ignoring case; any mismatch -> not a palindrome.
    No need to build a cleaned copy of the string.

Complexity:
    Time:  O(n)  - each char is visited once
    Space: O(1)  - just two pointers
"""


class Solution:
    def isPalindrome(self, s: str) -> bool:
        if len(s) == 1:
            return True

        left, right = 0, len(s) - 1

        while left < right:
            while left < right and not s[left].isalnum():
                left += 1

            while left < right and not s[right].isalnum():
                right -= 1

            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1

        return True


if __name__ == "__main__":
    sol = Solution()
    assert sol.isPalindrome("A man, a plan, a canal: Panama") is True
    assert sol.isPalindrome("race a car") is False
    assert sol.isPalindrome(" ") is True
    assert sol.isPalindrome("0P") is False
    assert sol.isPalindrome(".,") is True
    assert sol.isPalindrome("a") is True
    print("All tests passed.")
