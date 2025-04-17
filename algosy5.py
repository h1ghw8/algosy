#1
import datetime

def add_years(d, years):
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d.replace(month=2, day=28, year=d.year + years)

def main():
    n = int(input())
    events = []  
    for _ in range(n):
        vals = list(map(int, input().split()))
        bd, bm, by = vals[0], vals[1], vals[2]
        dd, dm, dy = vals[3], vals[4], vals[5]
        birth = datetime.date(by, bm, bd)
        death = datetime.date(dy, dm, dd)
        start = add_years(birth, 18)  
        end80 = add_years(birth, 80)
        end = min(end80, death)
        if start >= end:
            continue
        events.append((start, 1))
        events.append((end, -1))
    
    events.sort(key=lambda x: (x[0], x[1]))
    
    current = ans = 0
    for _, delta in events:
        current += delta
        if current > ans:
            ans = current
    print(ans)

if __name__ == '__main__':
    main()

#2

import heapq

def main():
    n = int(input())
    k = int(input())

    minkheap = []
    for _ in range(k):
        num = int(input())
        heapq.heappush(minkheap, -num)  

    for _ in range(n - k):
        num = int(input())
        
        if -minkheap[0] > num:
        
            heapq.heapreplace(minkheap, -num)
    result = sorted([-x for x in minkheap])
    print(' '.join(map(str, result)))

if name == "main":
    main()


#3
def mergesortcount_inversions(arr):
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, invleft = mergesortcountinversions(arr[:mid])
    right, invright = mergesortcountinversions(arr[mid:])
    merged, invmerge = mergecount_inversions(left, right)
    return merged, invleft + invright + inv_merge

def mergecountinversions(left, right):
    i = j = 0
    merged = []
    inversions = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inversions += len(left) - i  
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inversions

def main():
    arr = []
    try:
        while True:
            line = input()
            if line:
                arr.append(int(line))
    except EOFError:
        pass
    , totalinversions = mergesortcount_inversions(arr)
    print(total_inversions)

if name == "main":
    main()
