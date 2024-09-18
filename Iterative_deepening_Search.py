# Directions for moving up, down, left, and right with labels
DIRECTIONS = [(0, 1, 'right'), (1, 0, 'down'), (0, -1, 'left'), (-1, 0, 'up')]

# Depth-Limited Search (DLS) for grid
def depth_limited_search(grid, start, goal, depth, visited):
    if start == goal:
        return True  # Goal found

    if depth == 0:
        return False  # Reached depth limit

    r, c = start
    visited[r][c] = True  # Mark as visited

    # Explore neighbors within the depth limit
    for dr, dc, direction in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and not visited[nr][nc] and grid[nr][nc] == 0:
            print(f"Exploring {direction} to ({nr}, {nc}) at depth {depth}")
            if depth_limited_search(grid, (nr, nc), goal, depth - 1, visited):
                return True

    visited[r][c] = False  # Backtrack
    return False  # Goal not found in this branch

# Iterative Deepening Search (IDS)
def iterative_deepening_search(grid, start, goal):
    depth = 0
    while True:
        print(f"\nTrying depth limit: {depth}")
        visited = [[False] * len(grid[0]) for _ in range(len(grid))]
        if depth_limited_search(grid, start, goal, depth, visited):
            return depth  # Goal found at this depth
        depth += 1

if __name__ == "__main__":
    # Define a grid where 0 is a path and 1 is an obstacle
    grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)  # Starting point
    goal = (4, 4)   # Goal point

    print(f"Iterative Deepening Search from {start} to {goal}:")
    result = iterative_deepening_search(grid, start, goal)
    print(f"\nGoal found at depth: {result}")
