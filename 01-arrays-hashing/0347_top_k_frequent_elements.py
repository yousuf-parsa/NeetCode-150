"""
LeetCode 347. Top K Frequent Elements
https://leetcode.com/problems/top-k-frequent-elements/
Difficulty: Medium

Intuition:
    First I count how many times each number appears, using a dict.
    Then, k times: I pick the number with the highest count,
    add it to the result, and delete it so the next max is the next most frequent.

Complexity:
    Time:  O(n + k*u)  - counting is O(n); each max() scans u unique numbers
    Space: O(u)        - the count dict
"""


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        count = {}
        for x in nums:
            count[x] = count.get(x, 0) + 1
        result = []
        for _ in range(k):
            best = max(count, key=count.get)
            result.append(best)
            del count[best]
        return result


if __name__ == "__main__":
    sol = Solution()
    assert sorted(sol.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert sol.topKFrequent([1], 1) == [1]
    assert sorted(sol.topKFrequent([4, 4, 5, 5, 5, 6], 2)) == [4, 5]
    assert sorted(sol.topKFrequent([-1, -1, 2, 3], 1)) == [-1]
    print("All tests passed.")
