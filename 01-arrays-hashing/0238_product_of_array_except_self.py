"""
LeetCode 238. Product of Array Except Self
https://leetcode.com/problems/product-of-array-except-self/
Difficulty: Medium

Intuition:
    Division isn't allowed, and multiplying everything for each i is O(n^2).
    Answer at i = (product of everything left of i) * (product of everything right of i).
    First pass, left to right: store the running left product in ans.
    Second pass, right to left: multiply in the running right product.

Complexity:
    Time:  O(n)  - two passes
    Space: O(1)  - besides the output array
"""


class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        ans = [1] * n

        prefix = 1
        for i in range(n):
            ans[i] = prefix
            prefix *= nums[i]

        suffix = 1

        for i in range(n - 1, -1, -1):
            ans[i] *= suffix
            suffix *= nums[i]

        return ans


if __name__ == "__main__":
    sol = Solution()
    assert sol.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert sol.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert sol.productExceptSelf([2, 3]) == [3, 2]
    assert sol.productExceptSelf([0, 0]) == [0, 0]
    print("All tests passed.")
