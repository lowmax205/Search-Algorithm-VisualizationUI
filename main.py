import tkinter as tk
from tkinter import messagebox
import time
import math

from algorithm.gbfs import GBFSLogic
from algorithm.bfs import BFSLogic
from algorithm.dfs import DFSLogic

NODE_RADIUS = 20
time_seconds = 0.5

class TreeVisualizer:
    start_count = 0

    def __init__(self, root):
        self.root = root
        self.root.title("Search Algorithm Visualization")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        self.canvas = tk.Canvas(self.main_frame, width=600, height=500)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)

        # Set the positions of the nodes
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
        self.selected_algorithm = tk.StringVar()
        self.selected_algorithm.set("GBFS")

        tk.Label(self.main_frame, text="Select Algorithm:").grid(row=1, column=0, padx=5, pady=5)
        algorithm_menu = tk.OptionMenu(self.main_frame, self.selected_algorithm, "GBFS", "BFS", "DFS", command=self.update_algorithm)
        algorithm_menu.grid(row=1, column=1, padx=5, pady=5)

        self.logic = None
        self.update_algorithm("GBFS")
        self.draw_nodes()
        self.draw_edges()
        self.create_input_ui()

    def update_algorithm(self, algorithm_name):
        
        if algorithm_name == "GBFS":
            self.logic = GBFSLogic(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message
            )
            self.logic.set_positions(self.positions)
            self.logic.set_heuristics(self.heuristics)
            self.update_node_heuristics_display()

        elif algorithm_name == "BFS":
            self.clear_node_heuristics_display()
            self.logic = BFSLogic(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message
            )
            self.logic.set_positions(self.positions)
            

        elif algorithm_name == "DFS":
            self.clear_node_heuristics_display()
            self.logic = DFSLogic(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message
            )
            self.logic.set_positions(self.positions)
            

    def draw_nodes(self):
        for node, (x, y) in self.positions.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

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

    def create_circle(self, x, y, r, node):
        circle = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            outline="black", width=2, fill=self.logic.node_colors[node]
        )
        self.canvas.create_text(x, y, text=node, font=('Arial', 14, 'bold'))
        return circle

    def create_line(self, x1, y1, x2, y2, r):
        angle = math.atan2(y2 - y1, x2 - x1)
        start_x = x1 + r * math.cos(angle)
        start_y = y1 + r * math.sin(angle)
        end_x = x2 - r * math.cos(angle)
        end_y = y2 - r * math.sin(angle)
        line = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=2)
        self.edges.append(line)

    def update_node_color(self, node, color):
        if node in self.nodes:
            self.logic.node_colors[node] = color
            self.canvas.itemconfig(self.nodes[node], fill=color)
            self.root.update()
            time.sleep(time_seconds)

    def show_goal_message(self, goal_node):
        messagebox.showinfo("Goal Reached", f"Goal node '{goal_node}' reached!")

    def create_input_ui(self):
        tk.Label(self.main_frame, text="Start Node:").grid(row=2, column=0, padx=5, pady=5)
        self.start_node_entry = tk.Entry(self.main_frame, width=5)
        self.start_node_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.main_frame, text="Goal Node (Optional):").grid(row=3, column=0, padx=5, pady=5)
        self.goal_node_entry = tk.Entry(self.main_frame, width=5)
        self.goal_node_entry.grid(row=3, column=1, padx=5, pady=5)

        self.start_button = tk.Button(self.main_frame, text="Start", command=self.start_function)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

    def validate_input(self, node):
        valid_nodes = set(self.positions.keys())
        return node in valid_nodes

    def start_function(self):
        start_node = self.start_node_entry.get().strip().upper()
        goal_node = self.goal_node_entry.get().strip().upper()
        
        print("START COUNT: ", TreeVisualizer.start_count)
        
        if TreeVisualizer.start_count != 0:
            self.logic.reset_colors()
            # Clear heuristic texts when resetting colors

        if not self.validate_input(start_node):
            messagebox.showerror("Error", "Invalid start node. Please enter a valid node.")
            return

        if goal_node and not self.validate_input(goal_node):
            messagebox.showerror("Error", "Invalid goal node. Please enter a valid node or leave blank.")
            return

        if isinstance(self.logic, GBFSLogic):
            self.heuristics = self.original_heuristics.copy()
            if goal_node:
                self.heuristics[goal_node] = 0
                self.logic.set_heuristics(self.heuristics)
                self.update_node_heuristics_display()

            self.logic.greedy_bfs(start_node, goal_node)

        elif isinstance(self.logic, BFSLogic):
            self.logic.bfs(start_node, goal_node)

        elif isinstance(self.logic, DFSLogic):
            self.logic.dfs(start_node, goal_node)

        TreeVisualizer.start_count += 1

    def update_node_heuristics_display(self):
            for node, (x, y) in self.positions.items():
                if node in self.heuristic_texts:
                    self.canvas.delete(self.heuristic_texts[node])
                heuristic_value = self.heuristics.get(node, "")
                self.heuristic_texts[node] = self.canvas.create_text(
                    x, y + NODE_RADIUS + 10, text=str(heuristic_value), font=('Arial', 12)
                )

    def clear_node_heuristics_display(self):
        for node, text_id in self.heuristic_texts.items():
            self.canvas.delete(text_id)
        self.heuristic_texts.clear()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    visualizer = TreeVisualizer(root)
    visualizer.run()
