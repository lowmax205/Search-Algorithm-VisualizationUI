import tkinter as tk
from tkinter import messagebox
import time
import math

from uninformed.bfs import BFSLogic
from uninformed.dfs import DFSLogic
from uninformed.dls import DFS_DLSLogic
from uninformed.ids import IDSLogic
from uninformed.ucs import UCSLogic

from informed.gbfs import GBFSLogic

FONT = ('Arial', 14, 'bold')
NODE_RADIUS = 20
time_seconds = 0

# Class for visualizing the tree and search algorithms
class TreeVisualizer:
    start_count = 0

    def __init__(self, root):
        # Initialize the main window and set its title
        self.root = root
        self.root.title("Search Algorithm Visualization")

        # Create the main frame to hold the canvas and other UI elements
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        # Create a canvas for drawing the tree structure (nodes and edges)
        self.canvas = tk.Canvas(self.main_frame, width=600, height=500)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)

        # Define the positions for nodes in the tree (fixed coordinates for visualization)
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

        # Define heuristics for Greedy Best-First Search (GBFS) or other heuristic-based algorithms
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
        self.heuristic_texts = {} 
        self.nodes = {} 
        self.edges = []
        
        # Holds the selected algorithm
        self.selected_uninformed_algorithm = tk.StringVar()  
        self.selected_uninformed_algorithm.set("None")  
        self.selected_informed_algorithm = tk.StringVar()
        self.selected_informed_algorithm.set("None") 

        # Dropdown menu to select an uninformed algorithm
        tk.Label(self.main_frame, text="Select Uninformed Algorithm:").grid(row=1, column=0, padx=5, pady=5)
        uninformed_menu = tk.OptionMenu(self.main_frame, self.selected_uninformed_algorithm, "None", "BFS", "DFS", "DLS", "IDS", "UCS", command=self.update_algorithm)
        uninformed_menu.grid(row=1, column=1, padx=5, pady=5)

        # Dropdown menu to select an informed algorithm (for now just GBFS)
        tk.Label(self.main_frame, text="Select Informed Algorithm:").grid(row=2, column=0, padx=5, pady=5)
        informed_menu = tk.OptionMenu(self.main_frame, self.selected_informed_algorithm, "None", "GBFS", "A-star", command=self.update_algorithm)
        informed_menu.grid(row=2, column=1, padx=5, pady=5)

        # Initialize the algorithm logic (default to BFS)
        self.logic = None
        self.update_algorithm("BFS")
        
        # Draw the tree's nodes and edges
        self.draw_nodes()
        self.draw_edges()

        # Create the user input interface (start node, goal node)
        self.create_input_ui()

    # Update the selected algorithm logic when the user chooses a different algorithm
    def update_algorithm(self, algorithm_name):
        # Reset any cost display for UCS when switching algorithms
        if algorithm_name != "UCS":
            self.reset_cost_display()
            
            
            
            # Switch between different algorithm logic classes
            if algorithm_name == "BFS":
                self.set_algorithm_logic(BFSLogic)
            elif algorithm_name == "DFS":
                self.set_algorithm_logic(DFSLogic)
            elif algorithm_name == "DLS":
                self.set_algorithm_logic(DFS_DLSLogic)
            elif algorithm_name == "IDS":
                self.set_algorithm_logic(IDSLogic)
            elif algorithm_name == "UCS":
                self.set_algorithm_logic(UCSLogic)
            elif algorithm_name == "GBFS":
                self.set_algorithm_logic(GBFSLogic, clear_heuristics=False)
                self.logic.set_heuristics(self.heuristics)
                self.update_node_heuristics_display()
                
    # Set the logic for the chosen algorithm and clear heuristic display if needed
    def set_algorithm_logic(self, LogicClass, clear_heuristics=True):
        if clear_heuristics:
            self.clear_node_heuristics_display()
        
        # Special case for UCS to include cost display functionality
        if LogicClass == UCSLogic:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message,
                update_cost_display=self.update_cost_display
            )
        else:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message
            )
        
        # Set positions for the algorithm logic to reference
        self.logic.set_positions(self.positions)

    # Draw the nodes on the canvas as circles
    def draw_nodes(self):
        for node, (x, y) in self.positions.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

    # Draw the edges (connections between nodes) on the canvas
    def draw_edges(self):
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

    # Helper method to create a circle (node) on the canvas
    def create_circle(self, x, y, r, node):
        circle = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            outline="black", width=2, fill=self.logic.node_colors[node]
        )
        self.canvas.create_text(x, y, text=node, font=FONT)
        return circle

    # Helper method to create a line (edge) between two nodes on the canvas
    def create_line(self, x1, y1, x2, y2, r):
        angle = math.atan2(y2 - y1, x2 - x1)
        start_x = x1 + r * math.cos(angle)
        start_y = y1 + r * math.sin(angle)
        end_x = x2 - r * math.cos(angle)
        end_y = y2 - r * math.sin(angle)
        line = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=2)
        self.edges.append(line)

    # Update the color of a node during the algorithm's execution
    def update_node_color(self, node, color, animate=True):
        if node in self.nodes:
            self.logic.node_colors[node] = color
            self.canvas.itemconfig(self.nodes[node], fill=color)
            if animate:
                self.root.update()
                time.sleep(time_seconds)  # Delay to simulate animation

    # Display a message when the goal node is reached
    def show_goal_message(self, goal_node):
        messagebox.showinfo("Goal Reached", f"Goal node '{goal_node}' reached!")

    # Create the input interface for users to select the start and goal nodes
    def create_input_ui(self):
        tk.Label(self.main_frame, text="Start Node:").grid(row=3, column=0, padx=5, pady=5)
        self.start_node_entry = tk.Entry(self.main_frame, width=5)
        self.start_node_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.main_frame, text="Goal Node (Optional):").grid(row=4, column=0, padx=5, pady=5)
        self.goal_node_entry = tk.Entry(self.main_frame, width=5)
        self.goal_node_entry.grid(row=4, column=1, padx=5, pady=5)

        self.start_button = tk.Button(self.main_frame, text="Start", command=self.start_function)
        self.start_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Validate user input to ensure it's a valid node in the tree
    def validate_input(self, node):
        valid_nodes = set(self.positions.keys())
        return node in valid_nodes

    # Start the selected search algorithm based on user input
    def start_function(self):
        start_node = self.start_node_entry.get().strip().upper()
        goal_node = self.goal_node_entry.get().strip().upper()

        print("START COUNT: ", TreeVisualizer.start_count)
        
        # Reset color and cost display if this is not the first run
        if TreeVisualizer.start_count != 0:
            self.reset_cost_display()
            self.logic.reset_colors()

        # Check if the start node is valid
        if start_node not in self.positions:
            messagebox.showerror("Error", "Invalid start node. Please enter a valid node.")
            return

        # Check if the goal node is valid (if provided)
        if goal_node and not self.validate_input(goal_node):
            messagebox.showerror("Error", "Invalid goal node. Please enter a valid node or leave blank.")
            return
        
        # Determine if the user has selected an uninformed or informed algorithm
        uninformed_algorithm = self.selected_uninformed_algorithm.get()
        informed_algorithm = self.selected_informed_algorithm.get()

        # Ensure only one type of algorithm is selected (either uninformed or informed)
        if uninformed_algorithm != "None" and informed_algorithm == "None":
            # Run the appropriate uninformed search algorithm
            if uninformed_algorithm == "BFS":
                self.logic.bfs(start_node, goal_node)
            elif uninformed_algorithm == "DFS":
                self.logic.dfs(start_node, goal_node)
            elif uninformed_algorithm == "DLS":
                self.logic.dls(start_node, goal_node)
            elif uninformed_algorithm == "IDS":
                self.logic.ids(start_node, goal_node)
            elif uninformed_algorithm == "UCS":
                self.logic.ucs(start_node, goal_node)

        elif uninformed_algorithm == "None" and informed_algorithm != "None":
            # Run the appropriate informed search algorithm
            if informed_algorithm == "GBFS":
                self.heuristics = self.original_heuristics.copy()
                if goal_node:
                    self.heuristics[goal_node] = 0
                    self.logic.set_heuristics(self.heuristics)
                    self.update_node_heuristics_display()
                self.logic.greedy_bfs(start_node, goal_node)

        else:
            # If both or neither algorithms are selected, show an error message
            messagebox.showerror("Error", "Please select only one algorithm type: either Uninformed or Informed.")

        TreeVisualizer.start_count += 1

    # Update the display of node heuristic values (used in heuristic-based algorithms)
    def update_node_heuristics_display(self):
        for node, (x, y) in self.positions.items():
            if node in self.heuristic_texts:
                self.canvas.delete(self.heuristic_texts[node])
            heuristic_value = self.heuristics.get(node, "")
            self.heuristic_texts[node] = self.canvas.create_text(
                x, y + NODE_RADIUS + 10, text=str(heuristic_value), font=('Arial', 12)
            )

    # Clear the heuristic values from the canvas when not needed
    def clear_node_heuristics_display(self):
        for node, text_id in self.heuristic_texts.items():
            self.canvas.delete(text_id)
        self.heuristic_texts.clear()

    # Reset the cost display (used for UCS) before running the algorithm again
    def reset_cost_display(self):
        if hasattr(self.logic, 'cost_text_ids') and self.logic.cost_text_ids:
            for node in self.nodes:
                if node in self.logic.cost_text_ids:
                    self.canvas.delete(self.logic.cost_text_ids[node])
            self.logic.cost_text_ids.clear()

    # Update the cost display for UCS (when visiting a node)
    def update_cost_display(self, node, cost):
        if node in self.nodes:
            if node in self.logic.cost_text_ids:
                self.canvas.delete(self.logic.cost_text_ids[node])
            x, y = self.positions[node]
            text_id = self.canvas.create_text(x, y + NODE_RADIUS + NODE_RADIUS, text=str(cost), font=('Arial', 10))
            self.logic.cost_text_ids[node] = text_id
            self.canvas.itemconfig(self.nodes[node], fill=self.logic.node_colors[node])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk() 
    visualizer = TreeVisualizer(root) 
    visualizer.run() 
