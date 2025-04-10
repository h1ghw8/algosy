#1

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def quicksort(nums):
            if len(nums)<=1:
                return nums
            
            pivot = nums[random.randint(0, len(nums)-1)]
            left = []
            right = [] 
            mid = []

            for i in range(len(nums)):
                if nums[i] < pivot:
                    left.append(nums[i])
                elif nums[i] > pivot:
                    right.append(nums[i])
                else:
                    mid.append(nums[i])
            
            return quicksort(left)+mid+quicksort(right)
        
        return quicksort(nums)


#2

def merge_sort(points):
    if len(points) <= 1:
        return points
    mid = len(points) // 2
    left = merge_sort(points[:mid])
    right = merge_sort(points[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i][0] < right[j][0] or (left[i][0] == right[j][0] and left[i][1] < right[j][1]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

#3

def database(data):
    N = int(data[0])
    k = int(data[1])
    priority = list(map(int, data[2:2+k]))
    records = []
    index = 2 + k
    for _ in range(N):
        name = data[index]
        values = list(map(int, data[index+1:index+1+k]))
        records.append((name, values))
        index += 1 + k
    records.sort(key=lambda rec: tuple(rec[1][p-1] for p in priority))
    for rec in records:
        print(rec[0])
