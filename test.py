from typing import List


class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        out = [] 

        # nums1 = [0,0,0], m = 3
        # nums2 = [], n = 3
        # out = [1, 2, 2, 3, 5, 6]
        # i = 5
        for i in range(m+n):
            print(i, out)
            if len(nums1) <= m:
                out.append(nums2.pop(0))
            elif len(nums2) == 0:
                out.append(nums1.pop(0))
            else:
                if nums1[0] > nums2[0]:
                    out.append(nums2.pop(0))
                else:
                    out.append(nums1.pop(0))
        print(out)
        nums1 = out.copy()
        return

nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [2,5,6]
n = 3
answer = Solution()
answer.merge(nums1, m, nums2, n)
