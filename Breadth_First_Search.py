from collections import deque

# Directions for moving up, down, left, and right with labels
DIRECTIONS = [(0, 1, 'right'), (1, 0, 'down'), (0, -1, 'left'), (-1, 0, 'up')]

def bfs(grid, start):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    result = []

    # Create a queue for BFS, start with the starting point
    queue = deque([start])

    # Mark the start cell as visited
    visited[start[0]][start[1]] = True
    result.append(start)

    # Loop until the queue is empty
    while queue:
        # Dequeue a point from the queue
        r, c = queue.popleft()
        print(f"Visiting node ({r}, {c})\n")

        # Explore all four possible directions
        for dr, dc, direction in DIRECTIONS:
            nr, nc = r + dr, c + dc

            # Check if the new position is within bounds, not visited, and not an obstacle
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 0:
                print(f"Moving {direction} to ({nr}, {nc})")
                queue.append((nr, nc))
                visited[nr][nc] = True
                result.append((nr, nc))

    return result

if __name__ == "__main__":
    # Define a grid where 0 is a path and 1 is an obstacle
    grid = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)  # Starting point for BFS

    print("BFS from start:", start)
    result = bfs(grid, start)
    print("\nFinal result:", result)
