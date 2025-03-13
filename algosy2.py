#1

class Solution:
    def trap(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        left_max, right_max = 0, 0
        water_trapped = 0

        while left < right:
            if height[left] < height[right]:
                left_max = max(left_max, height[left])
                water_trapped += left_max - height[left]
                left += 1
            else:
                right_max = max(right_max, height[right])
                water_trapped += right_max - height[right]
                right -= 1

        return water_trapped

#2

class Solution:
    def simplifyPath(self, path: str) -> str:
        parts = path.split('/')
        stack = []
        
        for part in parts:
            if part == '' or part == '.':
                continue
            elif part == '..':
                if stack:
                    stack.pop()
            else:
                stack.append(part)
                
        simplified_path = '/' + '/'.join(stack)
        return simplified_path

#3


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = []
        max_area = 0
        heights.append(0)

        for i, h in enumerate(heights):
            while stack and heights[stack[-1]] > h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                max_area = max(max_area, height * width)
            stack.append(i)

        return max_area

#4

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0) 
        dummy.next = head
        prev = dummy
        
        while head:
            if head.next and head.val == head.next.val:
                while head.next and head.val == head.next.val:
                    head = head.next
                prev.next = head.next
            else:
                prev = prev.next
            head = head.next  
            
        return dummy.next

#5
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        dummy = ListNode(0)  
        current = dummy  
        
        while list1 and list2:
            if list1.val < list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            current = current.next  
            
        if list1:
            current.next = list1
        if list2:
            current.next = list2
        
        return dummy.next  

    
