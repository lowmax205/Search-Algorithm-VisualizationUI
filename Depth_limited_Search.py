# Directions for moving up, down, left, and right with labels
DIRECTIONS = [(0, 1, 'right'), (1, 0, 'down'), (0, -1, 'left'), (-1, 0, 'up')]

def dls_rec(grid, visited, r, c, depth, limit, result):
    rows, cols = len(grid), len(grid[0])

    # If the current depth exceeds the limit, return
    if depth > limit:
        return

    # Mark the current node as visited
    visited[r][c] = True
    print(f"Visiting node ({r}, {c}) at depth {depth}")
    result.append((r, c))  # Add the current node to the result list

    # Explore all four possible directions
    for dr, dc, direction in DIRECTIONS:
        nr, nc = r + dr, c + dc

        # Check if the new position is within bounds, not visited, and not an obstacle
        if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc] and grid[nr][nc] == 0:
            print(f"Moving {direction} to ({nr}, {nc})")
            dls_rec(grid, visited, nr, nc, depth + 1, limit, result)


def dls(grid, start, limit):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    result = []  # Initialize the result list

    # Call the recursive DLS function
    dls_rec(grid, visited, start[0], start[1], 0, limit, result)
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

    start = (0, 0)  # Starting point for DLS
    depth_limit = 2  # Define a depth limit for the search

    print(f"Depth-Limited Search from start: {start} with limit {depth_limit}")
    result = dls(grid, start, depth_limit)
    print("\nFinal result:", result)
