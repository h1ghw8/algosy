from collections import deque

def parse_maze_robots(maze_str):
    maze = []
    robot_a = robot_b = finish = None
    lines = maze_str.strip().split('\n')
    for i, line in enumerate(lines):
        row = list(line)
        maze.append(row)
        for j, cell in enumerate(row):
            if cell == 'A':
                robot_a = (i, j)
            elif cell == 'B':
                robot_b = (i, j)
            elif cell == 'F':
                finish = (i, j)
    return maze, robot_a, robot_b, finish

def bfs_dist(maze, start):
    rows, cols = len(maze), len(maze[0])
    dist = [[float('inf')] * cols for _ in range(rows)]
    queue = deque()
    queue.append(start)
    dist[start[0]][start[1]] = 0
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if maze[nx][ny] != '#' and dist[nx][ny] == float('inf'):
                    dist[nx][ny] = dist[x][y] + 1
                    queue.append((nx, ny))
    return dist

def bfs_parent(maze, start):
    rows, cols = len(maze), len(maze[0])
    parent = [[(-1, -1) for _ in range(cols)] for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]
    queue = deque()
    queue.append(start)
    visited[start[0]][start[1]] = True
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny] and maze[nx][ny] != '#':
                    visited[nx][ny] = True
                    parent[nx][ny] = (x, y)
                    queue.append((nx, ny))
    return parent

def mark_path(maze, parent, start, end):
    x, y = end
    while (x, y) != start:
        if maze[x][y] == '.':
            maze[x][y] = 'o'
        x, y = parent[x][y]

def solve_two_robots(maze_str):
    maze, robot_a, robot_b, finish = parse_maze_robots(maze_str)
    rows, cols = len(maze), len(maze[0])
    
    dist_a = bfs_dist(maze, robot_a)
    dist_b = bfs_dist(maze, robot_b)
    dist_f = bfs_dist(maze, finish)
    
    best_meet = None
    best_sum = float('inf')
    
    for i in range(rows):
        for j in range(cols):
            if maze[i][j] != '#':
                cur_sum = dist_a[i][j] + dist_b[i][j] + dist_f[i][j]
                if cur_sum < best_sum:
                    best_sum = cur_sum
                    best_meet = (i, j)
    
    if best_meet is None:
        return None
    
    parent_a = bfs_parent(maze, robot_a)
    parent_b = bfs_parent(maze, robot_b)
    parent_m = bfs_parent(maze, best_meet)
    
    mark_path(maze, parent_a, robot_a, best_meet)
    mark_path(maze, parent_b, robot_b, best_meet)
    mark_path(maze, parent_m, best_meet, finish)
    
    if best_meet != finish:
        maze[best_meet[0]][best_meet[1]] = 'M'
    
    return maze