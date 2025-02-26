#task 1



class Solution:
    def FindMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged=nums1+nums2
        merged.sort()
        mid=len(merged)//2
        if len(merged)%2==0:
            return (merged[mid-1]+merged[mid])/2
        else:
            return merged[mid]


#task 2

def IfCanReach(n, k, max_jump, a):
    a = '1' + a + '0'
    pos = 0
    jumps = 0
    while pos < n:
        farthest = pos
        while farthest < n - 1 and a[farthest] == '1' and farthest - pos < max_jump:
            farthest += 1
        
        if farthest == pos:
            return False
            
        pos = farthest
        jumps += 1
        
        if jumps > k:
            return False
    
    return jumps <= k

def FindMinimumLongestJump(n, k, a):
    a = '1' + a + '0'
    left, right = 1, n
    result = n

    while left <= right:
        mid = (left + right) // 2
        if IfCanReach(n, k, mid, a):
            result = mid
            right = mid - 1
        else:
            left = mid + 1

    return result


#task 3

def FindDuplicate(A):
    if len(A) <= 1:
        return -1

    slow = A[0]
    fast = A[A[0]]
    
    while fast  != slow:
        slow = A[slow]
        fast = A[A[fast]]
        
    slow = 0

    while fast != slow:
        slow = A[slow]
        fast = A[fast]
        
    return slow
    



#task4


def LowerBound(A, x):
    left, right = 0, len(A)
    while left < right:
        mid = (left + right) // 2
        if A[mid] < x:
            left = mid + 1
        else:
            right = mid
    return left

def FindMinIndices(A, B):
    n = len(A)
    result = []
    
    for b in B:
        k = LowerBound(A, b)
        result.append(k)
    
    return result
