from collections import defaultdict, deque
from typing import List

def valid_arrangement(pairs: List[List[int]]) -> List[List[int]]:
    graph = defaultdict(list)
    degree = defaultdict(int)
    
    for u, v in pairs:
        graph[u].append(v)
        degree[u] += 1
        degree[v] -= 1
    
    start = pairs[0][0]
    for node, deg in degree.items():
        if deg == 1:
            start = node
            break
    
    path = []
    stack = [start]
    
    while stack:
        node = stack[-1]
        if graph[node]:
            next_node = graph[node].pop()
            stack.append(next_node)
        else:
            path.append(node)
            stack.pop()
    
    path.reverse()
    
    result = []
    for i in range(len(path) - 1):
        result.append([path[i], path[i + 1]])
    
    return result

def count_paths(n: int, start: int, end: int, graph: List[List[int]]) -> int:
    dist = [-1] * n
    cnt = [0] * n
    queue = deque()
    
    dist[start] = 0
    cnt[start] = 1
    queue.append(start)
    
    while queue:
        v = queue.popleft()
        
        for u in graph[v]:
            if dist[u] == -1:
                dist[u] = dist[v] + 1
                cnt[u] = cnt[v]
                queue.append(u)
            elif dist[u] == dist[v] + 1:
                cnt[u] += cnt[v]
    
    return cnt[end]

def kosaraju(n: int, edges: List[List[int]]) -> int:
    graph = [[] for _ in range(n)]
    reverse_graph = [[] for _ in range(n)]
    
    for u, v in edges:
        graph[u].append(v)
        reverse_graph[v].append(u)
    
    visited = [False] * n
    order = []
    
    def dfs1(v):
        visited[v] = True
        for u in graph[v]:
            if not visited[u]:
                dfs1(u)
        order.append(v)
    
    for i in range(n):
        if not visited[i]:
            dfs1(i)
    
    comp = [-1] * n
    comp_count = 0
    
    def dfs2(v, cl):
        comp[v] = cl
        for u in reverse_graph[v]:
            if comp[u] == -1:
                dfs2(u, cl)
    
    while order:
        v = order.pop()
        if comp[v] == -1:
            dfs2(v, comp_count)
            comp_count += 1
    
    if comp_count == 1:
        return 0
    
    in_degree = [0] * comp_count
    out_degree = [0] * comp_count
    
    for v in range(n):
        for u in graph[v]:
            if comp[v] != comp[u]:
                out_degree[comp[v]] += 1
                in_degree[comp[u]] += 1
    
    sources = sum(1 for i in range(comp_count) if in_degree[i] == 0)
    sinks = sum(1 for i in range(comp_count) if out_degree[i] == 0)
    
    return max(sources, sinks)

def find_itinerary(tickets: List[List[str]]) -> List[str]:
    graph = defaultdict(list)
    
    for from_airport, to_airport in tickets:
        graph[from_airport].append(to_airport)
    
    for airport in graph:
        graph[airport].sort()
    
    itinerary = []
    
    def dfs(airport):
        while graph[airport]:
            next_airport = graph[airport].pop(0)
            dfs(next_airport)
        itinerary.append(airport)
    
    dfs("JFK")
    itinerary.reverse()
    return itinerary

def find_circle_num(is_connected: List[List[int]]) -> int:
    n = len(is_connected)
    visited = [False] * n
    provinces = 0
    
    def dfs(city):
        visited[city] = True
        for neighbor in range(n):
            if is_connected[city][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor)
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
            provinces += 1
    
    return provinces
