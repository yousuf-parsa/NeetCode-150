"""
LeetCode 15. 3Sum
https://leetcode.com/problems/3sum/
Difficulty: Medium

Intuition:
    Trying every triplet is O(n^3), too slow.
    I sort first, fix nums[i], then find the other two with two pointers:
    sum too small -> move left up, too big -> move right down.
    I skip equal values to avoid duplicate triplets.
    If nums[i] > 0, everything after is positive too, so I stop.

Complexity:
    Time:  O(n^2)  - two pointers for each i (sorting is O(n log n))
    Space: O(1)    - besides the output (sort is in place)
"""


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        res = []
        nums.sort()

        for i in range(len(nums)):
            if nums[i] > 0:
                break
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            left, right = i + 1, len(nums) - 1

            while left < right:
                s = nums[i] + nums[left] + nums[right]

                if s == 0:
                    res.append([nums[i], nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                elif s < 0:
                    left += 1
                else:
                    right -= 1

        return res


if __name__ == "__main__":
    sol = Solution()

    def norm(triplets):
        return sorted(sorted(t) for t in triplets)

    assert norm(sol.threeSum([-1, 0, 1, 2, -1, -4])) == [[-1, -1, 2], [-1, 0, 1]]
    assert sol.threeSum([0, 1, 1]) == []
    assert sol.threeSum([0, 0, 0]) == [[0, 0, 0]]
    assert sol.threeSum([0, 0, 0, 0]) == [[0, 0, 0]]
    assert norm(sol.threeSum([-2, 0, 0, 2, 2])) == [[-2, 0, 2]]
    print("All tests passed.")
