# Directions for moving up, down, left, and right with labels
DIRECTIONS = [(0, 1, 'right'), (1, 0, 'down'), (0, -1, 'left'), (-1, 0, 'up')]

def dfs_rec(grid, visited, r, c, result):
    rows, cols = len(grid), len(grid[0])

    # Mark the current node as visited
    visited[r][c] = True
    print(f"Visiting node ({r}, {c})")
    result.append((r, c))  # Add the current node to the result list

    # Explore all four possible directions
    for dr, dc, direction in DIRECTIONS:
        nr, nc = r + dr, c + dc

        # Check if the new position is within bounds, not visited, and not an obstacle
        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 0:
            print(f"Moving {direction} to ({nr}, {nc})\n")
            dfs_rec(grid, visited, nr, nc, result)


def dfs(grid, start):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    result = []  # Initialize the result list

    # Call the recursive DFS function
    dfs_rec(grid, visited, start[0], start[1], result)
    return result  # Return the result list


if __name__ == "__main__":
    # Define a grid where 0 is a path and 1 is an obstacle
    grid = [
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)  # Starting point for DFS

    print("DFS from start:", start)
    result = dfs(grid, start)
    print("\nFinal result:", result)
