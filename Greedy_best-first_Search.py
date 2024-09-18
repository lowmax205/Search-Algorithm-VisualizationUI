import heapq

# Directions for moving up, down, left, and right with labels
DIRECTIONS = [(0, 1, 'right'), (1, 0, 'down'), (0, -1, 'left'), (-1, 0, 'up')]

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def greedy_best_first_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    pq = [(heuristic(start, goal), start)]  # Priority queue with (heuristic value, node)
    
    while pq:
        # Get the node with the smallest heuristic value
        current_heuristic, (r, c) = heapq.heappop(pq)

        # If the goal is reached, return the node
        if (r, c) == goal:
            print(f"Goal reached at {goal}")
            return (r, c)

        # Skip already visited nodes
        if visited[r][c]:
            continue

        # Mark the current node as visited
        visited[r][c] = True
        print(f"Expanding node ({r}, {c}) with heuristic {current_heuristic}")

        # Explore neighbors
        for dr, dc, direction in DIRECTIONS:
            nr, nc = r + dr, c + dc

            # Check if the new position is within bounds, not visited, and not an obstacle
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 0:
                new_heuristic = heuristic((nr, nc), goal)
                print(f"Moving {direction} to ({nr}, {nc}) with heuristic {new_heuristic}\n")
                heapq.heappush(pq, (new_heuristic, (nr, nc)))

    return None  # If the goal is not reachable

if __name__ == "__main__":
    # Define a grid where 0 is a path and 1 is an obstacle
    grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)  # Starting point for GBFS
    goal = (4, 4)   # Goal point

    print(f"Greedy Best-First Search from {start} to {goal}:")
    result = greedy_best_first_search(grid, start, goal)
    if result is not None:
        print(f"\nGoal {goal} found from {start}.")
    else:
        print(f"\nGoal {goal} could not be reached from {start}.")
