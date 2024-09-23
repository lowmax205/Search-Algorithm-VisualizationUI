import tkinter as tk
from tkinter import messagebox
import math
import time
from gbfs import GBFSLogic

NODE_RADIUS = 20
time_seconds = 5

class TreeVisualizer:
    start_count = 0
    
    def __init__(self, root):
        self.root = root
        self.root.title("Greedy Best-First Search Visualization")

        # Set up the logic backend
        self.logic = GBFSLogic(
            canvas=None,
            update_node_color=self.update_node_color,
            show_goal_message=self.show_goal_message
        )

        # Create a frame for user input and visualization
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Create the canvas for visualizing the tree
        self.canvas = tk.Canvas(self.main_frame, width=600, height=500)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)
        self.logic.canvas = self.canvas  # Link canvas to logic

        # Define node positions and set them in the logic
        self.positions = {
            'A': (300, 50),
            'B': (200, 150),
            'C': (400, 150),
            'D': (150, 250),
            'E': (250, 250),
            'F': (350, 250),
            'G': (450, 250),
            'H': (100, 350),
            'I': (200, 350),
            'J': (300, 350),
            'K': (400, 350),
            'L': (150, 450),
            'M': (250, 450),
            'N': (350, 450)
        }
        self.logic.set_positions(self.positions)

        # Set heuristic values for nodes
        self.original_heuristics = {
            'A': 0,
            'B': 5,
            'C': 2,
            'D': 6,
            'E': 4,
            'F': 4,
            'G': 5,
            'H': 7,
            'I': 5,
            'J': 3,
            'K': 1,
            'L': 8,
            'M': 4,
            'N': 3 
        }
        self.heuristics = self.original_heuristics.copy()
        self.logic.set_heuristics(self.heuristics)

        # Draw nodes and edges
        self.nodes = {}
        self.edges = []
        self.heuristic_texts = {}  # Dictionary to store heuristic text items
        self.draw_nodes()
        self.draw_edges()

        # Create input fields for the user
        self.create_input_ui()

    def draw_nodes(self):
        # Draw all the nodes on the canvas.
        for node, (x, y) in self.positions.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

    def draw_edges(self):
        # Draw edges between nodes.
        edges = [
            ('A', 'B'), ('A', 'C'),
            ('B', 'D'), ('B', 'E'),
            ('C', 'F'), ('C', 'G'),
            ('D', 'H'), ('D', 'I'),
            ('F', 'J'), ('F', 'K'),
            ('H', 'L'), ('I', 'M'), ('J', 'N')
        ]
        for start, end in edges:
            self.create_line(*self.positions[start], *self.positions[end], NODE_RADIUS)

    def create_circle(self, x, y, r, node):
        # Create a circle with node text and its heuristic value below.
        # Create the circle for the node
        circle = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            outline="black", width=2, fill=self.logic.node_colors[node]
        )
        
        # Create text inside the circle (node letter)
        self.canvas.create_text(x, y, text=node, font=('Arial', 14, 'bold'))
        
        # Create text below the circle for the heuristic value
        heuristic_value = self.heuristics.get(node, "")
        self.heuristic_texts[node] = self.canvas.create_text(
            x, y + r + 10, text=str(heuristic_value), font=('Arial', 12)
        )

        return circle

    def create_line(self, x1, y1, x2, y2, r):
        # Create a line between two circles avoiding overlap.
        angle = math.atan2(y2 - y1, x2 - x1)
        start_x = x1 + r * math.cos(angle)
        start_y = y1 + r * math.sin(angle)
        end_x = x2 - r * math.cos(angle)
        end_y = y2 - r * math.sin(angle)
        line = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=2)
        self.edges.append(line)

    def update_node_color(self, node, color):
        # Update the color of a specified node.
        self.logic.node_colors[node] = color
        self.canvas.itemconfig(self.nodes[node], fill=color)
        self.root.update()
        time.sleep(time_seconds)

    def show_goal_message(self, goal_node):
        # Show a message when the goal node is reached.
        messagebox.showinfo("Goal Reached", f"Goal node '{goal_node}' reached!")

    def create_input_ui(self):
        # Create input fields and buttons in the main window.
        tk.Label(self.main_frame, text="Start Node:").grid(row=1, column=0, padx=5, pady=5)
        self.start_node_entry = tk.Entry(self.main_frame, width=5)
        self.start_node_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.main_frame, text="Goal Node (Optional):").grid(row=2, column=0, padx=5, pady=5)
        self.goal_node_entry = tk.Entry(self.main_frame, width=5)
        self.goal_node_entry.grid(row=2, column=1, padx=5, pady=5)

        self.start_button = tk.Button(self.main_frame, text="Start", command=self.start_function)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

    def validate_input(self, node):
        # Validate if the node input is within the valid range.
        valid_nodes = set(self.positions.keys())
        return node in valid_nodes

    def start_function(self):
        # Handle the start button click.
        print("START COUNT: ", TreeVisualizer.start_count)
        if TreeVisualizer.start_count != 0:
            self.logic.reset_colors()
        TreeVisualizer.start_count += 1
        
        start_node = self.start_node_entry.get().strip().upper()
        goal_node = self.goal_node_entry.get().strip().upper()

        if not self.validate_input(start_node):
            messagebox.showerror("Error", "Invalid start node. Please enter a valid node (A-G).")
            return

        if goal_node and not self.validate_input(goal_node):
            messagebox.showerror("Error", "Invalid goal node. Please enter a valid node (A-G) or leave blank.")
            return
        # Reset heuristics to original values
        self.heuristics = self.original_heuristics.copy()
        
        # Update heuristic value to 0 for the specified goal node
        if goal_node:
            self.heuristics[goal_node] = 0
            self.logic.set_heuristics(self.heuristics)
            self.update_node_heuristics_display()

        self.logic.greedy_bfs(start_node, goal_node)

    def update_node_heuristics_display(self):
        # Update the displayed heuristic values after setting the goal node.
        # Clear and update heuristic values
        for node, (x, y) in self.positions.items():
            # Delete the existing heuristic text
            if node in self.heuristic_texts:
                self.canvas.delete(self.heuristic_texts[node])
            # Draw the updated heuristic value
            heuristic_value = self.heuristics.get(node, "")
            self.heuristic_texts[node] = self.canvas.create_text(
                x, y + NODE_RADIUS + 10, text=str(heuristic_value), font=('Arial', 12)
            )

    def run(self):
        # Run the main application.
        self.root.mainloop()

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    visualizer = TreeVisualizer(root)
    visualizer.run()
