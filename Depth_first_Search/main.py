import tkinter as tk
from tkinter import messagebox
import math
import time
from dfs import DFSLogic

NODE_RADIUS = 20
time_seconds = 0.5

class TreeVisualizer:
    start_count = 0
    
    def __init__(self, root):
        self.root = root
        self.root.title("Depth First Search Visualization")

        # Set up the logic backend
        self.logic = DFSLogic(
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

        # Draw nodes and edges
        self.nodes = {}
        self.edges = []
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

    def create_circle(self, x, y, r, text):
        # Create a circle with text inside and return the canvas object.
        circle = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            outline="black", width=2, fill=self.logic.node_colors[text]
            )
        self.canvas.create_text(x, y, text=text, font=('Arial', 14, 'bold'))
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
        if node in self.nodes:
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
            messagebox.showerror("Error", "Invalid start node. Please enter a valid node.")
            return

        if goal_node and not self.validate_input(goal_node):
            messagebox.showerror("Error", "Invalid goal node. Please enter a valid node or leave blank.")
            return
        self.logic.dfs(start_node, goal_node)

    def run(self):
        # Run the main application.
        self.root.mainloop()


# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    visualizer = TreeVisualizer(root)
    visualizer.run()
