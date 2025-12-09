from collections import deque

def parse_map(map_str):
    return [list(line) for line in map_str.strip().split('\n')]

def time_to_flood(map_grid):
    rows, cols = len(map_grid), len(map_grid[0])
    queue = deque()
    
    for i in range(rows):
        for j in range(cols):
            if map_grid[i][j] == 'W':
                queue.append((i, j))
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    time = 0
    
    while queue:
        size = len(queue)
        flooded = False
        for _ in range(size):
            x, y = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if map_grid[nx][ny] == 'L':
                        map_grid[nx][ny] = 'W'
                        queue.append((nx, ny))
                        flooded = True
        if flooded:
            time += 1
    
    return time