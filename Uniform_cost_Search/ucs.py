import heapq

# Directions for moving up, down, left, and right
DIRECTIONS = [(0, 1, 'right'), (1, 0, 'down'), (0, -1, 'left'), (-1, 0, 'up')]

# Uniform-Cost Search function
def uniform_cost_search(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    # Priority queue to store (cost, node)
    pq = [(0, start)]  # (cost, (row, col)) pair
    visited = [[False] * cols for _ in range(rows)]
    cost_to_node = {start: 0}

    while pq:
        current_cost, (r, c) = heapq.heappop(pq)

        # If we reach the goal node, return the cost
        if (r, c) == goal:
            print(f"Goal reached at {goal} with cost {current_cost}")
            return current_cost

        # If the node has been visited, skip it
        if visited[r][c]:
            continue

        # Mark the current node as visited
        visited[r][c] = True
        print(f"Expanding node ({r}, {c}) with current cost {current_cost}")

        # Explore neighbors
        for dr, dc, direction in DIRECTIONS:
            nr, nc = r + dr, c + dc

            # Check if the new position is within bounds, not visited, and not an obstacle
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 0:
                new_cost = current_cost + 1  # Uniform cost of 1 for each move
                if new_cost < cost_to_node.get((nr, nc), float('inf')):
                    cost_to_node[(nr, nc)] = new_cost
                    heapq.heappush(pq, (new_cost, (nr, nc)))
                    print(f"Moving {direction} to ({nr}, {nc}) with new cost {new_cost}\n")

    return float('inf')  # If no path is found to the goal

if __name__ == "__main__":
    # Define a grid where 0 is a path and 1 is an obstacle
    grid = [
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)  # Starting point for UCS
    goal = (4, 4)   # Goal point

    print(f"Uniform-Cost Search from {start} to {goal}:")
    result = uniform_cost_search(grid, start, goal)
    print(f"\nCost to reach goal {goal} from {start}: {result}")
