import tkinter as tk
from tkinter import messagebox
import numpy as np
import heapq

# A* Algorithm Functions
class AStar:
    def __init__(self, grid, start, end):
        # Initialize the A* algorithm with the grid, start, and end points
        self.grid = grid
        self.start = start
        self.end = end
        self.rows = len(grid)  # Get number of rows in the grid
        self.cols = len(grid[0])  # Get number of columns in the grid
    
    def heuristic(self, a, b):
        # Calculate the Manhattan distance between points a and b as the heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def astar_search(self):
        # Perform the A* search algorithm
        open_list = []  # Priority queue of open nodes
        heapq.heappush(open_list, (0, self.start))  # Add the start node to the open list
        came_from = {}  # Dictionary to keep track of the path
        g_score = {self.start: 0}  # G-score for each node (cost from start)
        f_score = {self.start: self.heuristic(self.start, self.end)}  # F-score (g + heuristic)

        while open_list:
            _, current = heapq.heappop(open_list)  # Get the node with the lowest f-score

            if current == self.end:
                # If we've reached the end, reconstruct the path
                return self.reconstruct_path(came_from)

            # Explore all valid neighbors of the current node
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1  # Assume equal cost for all edges

                # If this path to the neighbor is better than any previous one
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current  # Update the path to reach this neighbor
                    g_score[neighbor] = tentative_g_score  # Update g-score for neighbor
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.end)  # Update f-score
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))  # Add neighbor to open list
        
        return None  # Return None if no path is found
    
    def reconstruct_path(self, came_from):
        # Reconstruct the path by backtracking from the end to the start
        path = []
        current = self.end
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(self.start)  # Add the start point
        path.reverse()  # Reverse the path to get it from start to end
        return path
    
    def get_neighbors(self, node):
        # Get all valid neighboring nodes of the current node
        neighbors = []
        x, y = node
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Move in 4 possible directions
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.grid[nx][ny] == 0:
                # Only consider neighbors within grid bounds and not blocked by obstacles
                neighbors.append((nx, ny))
        return neighbors

# UI Functions
class AStarUI:
    def __init__(self, root, rows=20, cols=20, cell_size=30):
        # Initialize the user interface for visualizing the A* algorithm
        self.root = root
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = np.zeros((rows, cols), dtype=int)  # Create an empty grid
        
        self.start = None  # Start point (set by user)
        self.end = None  # End point (set by user)
        
        # Create a canvas for the grid
        self.canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size)
        self.canvas.pack()
        
        # Bind mouse events for setting start, end, and obstacles
        self.canvas.bind("<Button-1>", self.on_left_click)  # Left-click to set the start point
        self.canvas.bind("<Button-3>", self.on_right_click)  # Right-click to set the end point
        self.canvas.bind("<B1-Motion>", self.on_drag)  # Drag to set obstacles
        
        self.draw_grid()  # Draw the initial empty grid
        
        # Button to run the A* algorithm
        self.run_button = tk.Button(root, text="Run", command=self.run_astar)
        self.run_button.pack(pady=10)

    def draw_grid(self):
        # Draw the grid with colors for start, end, and obstacles
        for i in range(self.rows):
            for j in range(self.cols):
                color = "white"  # Default cell color
                if self.grid[i][j] == 1:
                    color = "black"  # Obstacles are black
                elif (i, j) == self.start:
                    color = "green"  # Start point is green
                elif (i, j) == self.end:
                    color = "red"  # End point is red
                # Draw the rectangle (grid cell)
                self.canvas.create_rectangle(j * self.cell_size, i * self.cell_size, 
                                             (j+1) * self.cell_size, (i+1) * self.cell_size, 
                                             fill=color, outline="gray")
    
    def on_left_click(self, event):
        # Set the start point on left-click
        x, y = event.y // self.cell_size, event.x // self.cell_size
        if self.start is None:
            self.start = (x, y)
        else:
            self.grid[x][y] = 0  # Clear any obstacles at the start point
            self.start = (x, y)
        self.redraw()

    def on_right_click(self, event):
        # Set the end point on right-click
        x, y = event.y // self.cell_size, event.x // self.cell_size
        if self.end is None:
            self.end = (x, y)
        else:
            self.grid[x][y] = 0  # Clear any obstacles at the end point
            self.end = (x, y)
        self.redraw()

    def on_drag(self, event):
        # Set obstacles by dragging the mouse
        x, y = event.y // self.cell_size, event.x // self.cell_size
        if (x, y) != self.start and (x, y) != self.end:
            self.grid[x][y] = 1  # Mark the cell as an obstacle
        self.redraw()

    def redraw(self):
        # Redraw the entire grid (called after each change)
        self.canvas.delete("all")  # Clear the canvas
        self.draw_grid()  # Redraw the grid

    def run_astar(self):
        # Run the A* algorithm when the user clicks the "Run" button
        if self.start is None or self.end is None:
            messagebox.showerror("Error", "Start or End point is not set!")  # Show error if start/end is missing
            return
        
        astar = AStar(self.grid, self.start, self.end)  # Create an A* algorithm instance
        path = astar.astar_search()  # Run the A* algorithm to find the path
        
        if path:
            self.show_path(path)  # Display the path if found
        else:
            messagebox.showerror("Error", "No path found!")  # Show error if no path exists

    def show_path(self, path):
        # Highlight the path found by the A* algorithm
        for (x, y) in path:
            self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, 
                                         (y+1) * self.cell_size, (x+1) * self.cell_size, 
                                         fill="blue", outline="gray")  # Path cells are blue

# Main Application
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    root.title("A* Search Visualization")  # Set the window title
    
    app = AStarUI(root)  # Create an instance of the UI
    
    root.mainloop()  # Start the Tkinter event loop
