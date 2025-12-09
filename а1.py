from collections import deque

def shortest_path_all_keys(grid):
    rows, cols = len(grid), len(grid[0])
    start_x = start_y = -1
    key_mask = 0
    
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell == '@':
                start_x, start_y = i, j
            elif 'a' <= cell <= 'f':
                key_mask |= 1 << (ord(cell) - ord('a'))
    
    target_mask = key_mask
    visited = [[[False] * (1 << 6) for _ in range(cols)] for _ in range(rows)]
    visited[start_x][start_y][0] = True
    
    queue = deque()
    queue.append((start_x, start_y, 0))
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    steps = 0
    
    while queue:
        size = len(queue)
        for _ in range(size):
            x, y, mask = queue.popleft()
            
            if mask == target_mask:
                return steps
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    cell = grid[nx][ny]
                    if cell == '#':
                        continue
                    if 'A' <= cell <= 'F' and not (mask & (1 << (ord(cell) - ord('A')))):
                        continue
                    
                    new_mask = mask
                    if 'a' <= cell <= 'f':
                        new_mask |= 1 << (ord(cell) - ord('a'))
                    
                    if not visited[nx][ny][new_mask]:
                        visited[nx][ny][new_mask] = True
                        queue.append((nx, ny, new_mask))
        steps += 1
    
    return -1