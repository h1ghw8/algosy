from collections import deque

def parse_maze(maze_str):
    maze = []
    for line in maze_str.strip().split('\n'):
        maze.append(list(line))
    return maze

def find_exit(maze):
    rows, cols = len(maze), len(maze[0])
    start_x = start_y = -1
    
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] == 'S':
                start_x, start_y = i, j
                break
    
    visited = [[False] * cols for _ in range(rows)]
    parent = [[(-1, -1) for _ in range(cols)] for _ in range(rows)]
    queue = deque()
    queue.append((start_x, start_y))
    visited[start_x][start_y] = True
    
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    exit_x = exit_y = -1
    
    while queue:
        x, y = queue.popleft()
        
        if x == 0 or x == rows - 1 or y == 0 or y == cols - 1:
            exit_x, exit_y = x, y
            break
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny] and maze[nx][ny] != '#':
                    visited[nx][ny] = True
                    parent[nx][ny] = (x, y)
                    queue.append((nx, ny))
    
    if exit_x == -1:
        return None
    
    x, y = exit_x, exit_y
    while not (x == start_x and y == start_y):
        if maze[x][y] == '.':
            maze[x][y] = 'o'
        x, y = parent[x][y]
    
    return maze