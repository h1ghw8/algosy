import heapq

SIZE = 4

class State:
    def __init__(self, board, empty_row, empty_col, moves=""):
        self.board = board
        self.empty_row = empty_row
        self.empty_col = empty_col
        self.moves = moves
        self.score = 0
    
    def __lt__(self, other):
        return self.score < other.score
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True
    
    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board))

def is_solved(state):
    correct = 1
    for i in range(SIZE):
        for j in range(SIZE):
            if i == SIZE - 1 and j == SIZE - 1:
                if state.board[i][j] != 0:
                    return False
            else:
                if state.board[i][j] != correct:
                    return False
                correct += 1
    return True

def calc_distance(state):
    total = 0
    for i in range(SIZE):
        for j in range(SIZE):
            num = state.board[i][j]
            if num != 0:
                goal_row = (num - 1) // SIZE
                goal_col = (num - 1) % SIZE
                total += abs(i - goal_row) + abs(j - goal_col)
    return total

def calc_conflicts(state):
    conflicts = 0
    
    for row in range(SIZE):
        for col1 in range(SIZE):
            num1 = state.board[row][col1]
            if num1 == 0:
                continue
            goal_row1 = (num1 - 1) // SIZE
            if goal_row1 == row:
                for col2 in range(col1 + 1, SIZE):
                    num2 = state.board[row][col2]
                    if num2 == 0:
                        continue
                    goal_row2 = (num2 - 1) // SIZE
                    goal_col2 = (num2 - 1) % SIZE
                    if goal_row2 == row and goal_col2 < col1:
                        conflicts += 2
    
    for col in range(SIZE):
        for row1 in range(SIZE):
            num1 = state.board[row1][col]
            if num1 == 0:
                continue
            goal_col1 = (num1 - 1) % SIZE
            if goal_col1 == col:
                for row2 in range(row1 + 1, SIZE):
                    num2 = state.board[row2][col]
                    if num2 == 0:
                        continue
                    goal_row2 = (num2 - 1) // SIZE
                    goal_col2 = (num2 - 1) % SIZE
                    if goal_col2 == col and goal_row2 < row1:
                        conflicts += 2
    
    return conflicts

def calc_heuristic(state):
    return calc_distance(state) + calc_conflicts(state)

def can_solve(state):
    numbers = []
    for i in range(SIZE):
        for j in range(SIZE):
            if state.board[i][j] != 0:
                numbers.append(state.board[i][j])
    
    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                inversions += 1
    
    empty_from_bottom = SIZE - state.empty_row
    
    if empty_from_bottom % 2 == 0:
        return inversions % 2 == 1
    else:
        return inversions % 2 == 0

def find_solution(start):
    if not can_solve(start):
        return "No solution"
    
    queue = []
    start.score = calc_heuristic(start)
    heapq.heappush(queue, (start.score, 0, start))
    
    seen = set()
    counter = 1
    
    row_moves = [-1, 1, 0, 0]
    col_moves = [0, 0, -1, 1]
    move_names = ['U', 'D', 'L', 'R']
    
    while queue:
        _, _, current = heapq.heappop(queue)
        
        state_id = hash(current)
        if state_id in seen:
            continue
        seen.add(state_id)
        
        if is_solved(current):
            return current.moves
        
        for i in range(4):
            new_row = current.empty_row + row_moves[i]
            new_col = current.empty_col + col_moves[i]
            
            if 0 <= new_row < SIZE and 0 <= new_col < SIZE:
                new_board = [row[:] for row in current.board]
                new_board[current.empty_row][current.empty_col], new_board[new_row][new_col] = new_board[new_row][new_col], new_board[current.empty_row][current.empty_col]
                
                next_state = State(new_board, new_row, new_col, current.moves + move_names[i])
                
                if hash(next_state) not in seen:
                    path_cost = len(next_state.moves)
                    heuristic_cost = calc_heuristic(next_state)
                    next_state.score = path_cost + heuristic_cost
                    
                    heapq.heappush(queue, (next_state.score, counter, next_state))
                    counter += 1
    
    return "No solution"

def main():
    puzzle = [
        [5, 2, 7, 8],
        [9, 6, 3, 4],
        [1, 12, 14, 10],
        [13, 0, 11, 15]
    ]
    
    empty_r, empty_c = -1, -1
    for r in range(SIZE):
        for c in range(SIZE):
            if puzzle[r][c] == 0:
                empty_r, empty_c = r, c
    
    start_state = State(puzzle, empty_r, empty_c)
    
    result = find_solution(start_state)
    print(f"Solvable: {can_solve(start_state)}")
    if result == "No solution":
        print("No solution exists")
    else:
        print(f"Solution: {result}")
        print(f"Number of moves: {len(result)}")

if __name__ == "__main__":
    main()
