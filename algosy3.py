import heapq


#1
def min_sum_time(numbers):
    heapq.heapify(numbers)
    total_time = 0
    
    while len(numbers) > 1:
        first = heapq.heappop(numbers)
        second = heapq.heappop(numbers)
        
        current_time = first + second
        total_time += current_time
        
        heapq.heappush(numbers, current_time)
    
    return total_time

n = int(input())
numbers = [int(input()) for _ in range(n)]

result = min_sum_time(numbers)
print(result)


#2


def min_stations(n, schedule):
    if n == 0:
        return 0

    heap = []
    count = 0
    
    for arrival, departure in schedule:
        while heap and heap[0] < arrival:
            heapq.heappop(heap)
        heapq.heappush(heap, departure)
        count = max(count, len(heap))

    return count

n2 = int(input())
schedule = [tuple(map(int, input().split())) for _ in range(n2)]

print(min_stations(n2, schedule))

#3

def sliding_window_maximum(arr, k):
    if not arr or k == 0:
        return []
    
    n = len(arr)
    max_values = []
    max_heap = []
    
    for i in range(n):
        while max_heap and max_heap[0][1] <= i - k:
            heapq.heappop(max_heap)

        heapq.heappush(max_heap, (-arr[i], i))
        
        if i >= k - 1:
            max_values.append(-max_heap[0][0])
    
    return max_values

n3 = int(input())
arr = [int(input()) for _ in range(n3)]
k = int(input())

result3 = sliding_window_maximum(arr, k)
print(" ".join(map(str, result3)))


