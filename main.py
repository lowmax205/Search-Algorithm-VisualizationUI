import customtkinter as tk
import time
import math
from tkinter import messagebox
from PIL import Image, ImageTk
from source import ORIGINAL_HEURISTICS as heuristics_list

import sys
import os

from uninformed.bfs import BFSLogic
from uninformed.dfs import DFSLogic
from uninformed.dls import DFS_DLSLogic
from uninformed.ids import IDSLogic
from uninformed.ucs import UCSLogic

from informed.gbfs import GBFSLogic
from informed.astar import AStarLogic

FONT = ("Arial", 14, "bold")
NORMAL_FONT = ("Arial", 12)
SMALL_FONT = ("Arial", 10)
NODE_RADIUS = 20
TIME_SECONDS = 0.1


def resource_path(relative_path):
    # Get the absolute path to resources
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


icon_path = resource_path("assets/Searching.ico")


class TreeVisualizer:
    start_count = 0

    # Constructor for initializing the main window and its components
    def __init__(self, root):
        self.root = root
        self.root.title("Search Algorithm Visualization")
        self.root.iconbitmap(icon_path)
        self.node_lines = {}
        self.setup_theme()
        self.setup_main_frame()
        self.setup_positions()
        self.setup_graph_data()
        self.initialize_variables()
        self.create_algorithm_menus()
        self.setup_visualization()

    def setup_theme(self):
        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("dark-blue")

    def setup_main_frame(self):
        self.main_frame = tk.CTkFrame(self.root)
        self.main_frame.pack(pady=10)
        self.canvas = tk.CTkCanvas(self.main_frame)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)

    def setup_positions(self):
        self.positions_tree = {
            "A": (300, 50),
            "B": (200, 150),
            "C": (400, 150),
            "D": (150, 250),
            "E": (250, 250),
            "F": (350, 250),
            "G": (450, 250),
            "H": (100, 350),
            "I": (200, 350),
            "J": (300, 350),
            "K": (400, 350),
            "L": (150, 450),
            "M": (250, 450),
            "N": (350, 450),
        }

        scale_x, scale_y = 400 / 500, 300 / 500
        self.positions_star = {
            "A": (int(290 * scale_x), int(1100 * scale_y)),
            "B": (int(400 * scale_x), int(900 * scale_y)),
            "C": (int(980 * scale_x), int(100 * scale_y)),
            "D": (int(550 * scale_x), int(1000 * scale_y)),
            "E": (int(950 * scale_x), int(650 * scale_y)),
            "F": (int(820 * scale_x), int(450 * scale_y)),
            "G": (int(1050 * scale_x), int(510 * scale_y)),
            "H": (int(450 * scale_x), int(950 * scale_y)),
            "I": (int(200 * scale_x), int(900 * scale_y)),
            "J": (int(100 * scale_x), int(850 * scale_y)),
            "K": (int(980 * scale_x), int(400 * scale_y)),
            "L": (int(330 * scale_x), int(750 * scale_y)),
            "M": (int(830 * scale_x), int(290 * scale_y)),
            "N": (int(100 * scale_x), int(600 * scale_y)),
            "O": (int(1000 * scale_x), int(260 * scale_y)),
            "P": (int(850 * scale_x), int(180 * scale_y)),
            "Q": (int(230 * scale_x), int(750 * scale_y)),
            "R": (int(850 * scale_x), int(800 * scale_y)),
            "S": (int(200 * scale_x), int(500 * scale_y)),
            "T": (int(320 * scale_x), int(600 * scale_y)),
            "U": (int(330 * scale_x), int(900 * scale_y)),
        }

    def setup_graph_data(self):
        self.SURIGAO_DEL_NORTE_DISTANCE = {
            "A": 46.3,
            "B": 38.7,
            "C": 104,
            "D": 55.1,
            "E": 65.2,
            "F": 87.3,
            "G": 80.4,
            "H": 52.7,
            "I": 36.1,
            "J": 30.9,
            "K": 90.70,
            "L": 31.8,
            "M": 94.2,
            "N": 10.6,
            "O": 93.5,
            "P": 102,
            "Q": 19.3,
            "R": 95.7,
            "S": 0,
            "T": 23.5,
            "U": 35.2,
        }

        self.SURIGAO_DEL_NORTE_COST = {
            "A": 37.57,
            "B": 25.95,
            "C": 68.45,
            "D": 35.67,
            "E": 61.45,
            "F": 54.70,
            "G": 72.12,
            "H": 21.20,
            "I": 28.06,
            "J": 21.70,
            "K": 67.00,
            "L": 19.16,
            "M": 59.33,
            "N": 7.98,
            "O": 67.00,
            "P": 64.70,
            "Q": 15.30,
            "R": 52.22,
            "S": 0,
            "T": 14.35,
            "U": 27.67,
        }

        self.SURIGAO_DEL_NORTE = {
            "A": "Alegria",
            "B": "Bacuag",
            "C": "Burgos",
            "D": "Claver",
            "E": "Dapa",
            "F": "Del Carmen",
            "G": "General Luna",
            "H": "Gigaquit",
            "I": "Mainit",
            "J": "Malimono",
            "K": "Pilar",
            "L": "Placer",
            "M": "San Benito",
            "N": "San Francisco",
            "O": "San Isidro",
            "P": "Santa Monica",
            "Q": "Sison",
            "R": "Socorro",
            "S": "Surigao City",
            "T": "Tagana-an",
            "U": "Tubod",
        }

    def initialize_variables(self):
        self.heuristics = heuristics_list.copy()
        self.heuristic_texts = {}
        self.nodes = {}
        self.edges = []
        self.selected_uninformed_algorithm = tk.StringVar(value="None")
        self.selected_informed_algorithm = tk.StringVar(value="None")
        self.node_labels = {}
        self.current_highlighted = None

    def create_algorithm_menus(self):
        tk.CTkLabel(self.main_frame, text="Select Uninformed Algorithm:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        uninformed_menu = tk.CTkOptionMenu(
            self.main_frame,
            variable=self.selected_uninformed_algorithm,
            values=["None", "BFS", "DFS", "DLS", "IDS", "UCS"],
            command=self.update_algorithm,
        )
        uninformed_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.CTkLabel(self.main_frame, text="Select Informed Algorithm:").grid(
            row=2, column=0, padx=5, pady=5, sticky="e"
        )
        informed_menu = tk.CTkOptionMenu(
            self.main_frame,
            variable=self.selected_informed_algorithm,
            values=["None", "GBFS", "A-star"],
            command=self.update_algorithm,
        )
        informed_menu.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    def setup_visualization(self):
        self.logic = None
        self.update_algorithm("BFS")
        self.draw_nodes()
        self.draw_edges()
        self.create_legend()
        self.create_input_ui()
        self.canvas.bind("<Configure>", self.update_legend_position)

    # Update the selected algorithm and reconfigure the interface
    def update_algorithm(self, algorithm_name):

        if algorithm_name in ["BFS", "DFS", "DLS", "IDS", "UCS"]:
            self.selected_informed_algorithm.set("None")
        elif algorithm_name in ["GBFS", "A-star"]:
            self.selected_uninformed_algorithm.set("None")

        if algorithm_name != "UCS":
            self.reset_cost_display()

        if self.logic:
            self.logic.reset_colors()

        # if algorithm_name == "DLS":
        #     self.create_input_ui(depth_limit=True)
        # else:
        #     self.create_input_ui()

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
        elif algorithm_name == "A-star":
            self.set_algorithm_logic(AStarLogic)
            self.draw_graph()
        elif algorithm_name == "GBFS":
            self.set_algorithm_logic(GBFSLogic, clear_heuristics=False)
            self.logic.set_heuristics(self.heuristics)
            self.update_node_heuristics_display()

        if algorithm_name != "A-star":
            self.display_node_list(self.main_frame, False)

    # Set the logic for the selected algorithm and update the canvas
    def set_algorithm_logic(self, LogicClass, clear_heuristics=True):
        self.clear_canvas()

        if clear_heuristics:
            self.clear_node_heuristics_display()

        if LogicClass == UCSLogic:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message,
                update_cost_display=self.update_cost_display,
                node_lines=self.node_lines,
            )
            self.canvas.config(width=600, height=500)

            self.draw_nodes()
            self.draw_edges()

        elif LogicClass == AStarLogic:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message,
                node_lines=self.node_lines,
            )
            self.draw_graph()
            self.display_node_list(self.main_frame, True)

        else:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message,
                node_lines=self.node_lines,
            )
            self.canvas.config(width=600, height=500)
            self.clear_canvas()
            self.draw_nodes()
            self.draw_edges()

    # Create a legend explaining the color coding of nodes
    def create_legend(self):
        legend_items = [
            ("Start Node", "green"),
            ("Goal Node", "red"),
            ("Path Node", "blue"),
            ("Visited Node", "orange"),
            ("Visiting Node", "#806000"),
            ("Unvisited Node", "white"),
        ]

        legend_width = 150
        legend_height = len(legend_items) * 30 + 10
        legend_x = 10
        legend_y = 10

        self.canvas.create_rectangle(
            legend_x,
            legend_y,
            legend_x + legend_width,
            legend_y + legend_height,
            fill="lightgray",
            outline="black",
        )

        for i, (label, color) in enumerate(legend_items):
            y = legend_y + 20 + i * 30
            self.canvas.create_oval(
                legend_x + 10,
                y - 10,
                legend_x + 30,
                y + 10,
                fill=color,
                outline="black",
            )
            self.canvas.create_text(
                legend_x + 40, y, text=label, anchor="w", font=SMALL_FONT
            )

    # Draws nodes on the canvas
    def draw_nodes(self):
        self.create_legend()
        for node, (x, y) in self.positions_tree.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

    # Creates the edges of the tree and draws them on the canvas
    def draw_edges(self):
        edges = [
            ("A", "B"),
            ("A", "C"),
            ("B", "D"),
            ("B", "E"),
            ("C", "F"),
            ("C", "G"),
            ("D", "H"),
            ("D", "I"),
            ("F", "J"),
            ("F", "K"),
            ("H", "L"),
            ("I", "M"),
            ("J", "N"),
        ]
        self.draw_lines(edges, self.positions_tree)

    # Draw the graph for A* algorithm
    def draw_graph(self):
        # Load the background image
        image_path = "assets/map_image.jpg"
        image = Image.open(image_path)
        self.background_image = ImageTk.PhotoImage(image)

        # Configure canvas size to match image dimensions
        self.canvas.config(width=image.width, height=image.height)

        # Add the image to the canvas to fill entire space
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")

        self.create_legend()
        for node, (x, y) in self.positions_star.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

        edges = [
            ("S", "N"),
            ("S", "Q"),
            ("S", "T"),
            ("S", "E"),
            ("N", "J"),
            ("J", "I"),
            ("I", "U"),
            ("U", "A"),
            ("U", "L"),
            ("Q", "U"),
            ("T", "Q"),
            ("T", "L"),
            ("L", "B"),
            ("B", "H"),
            ("H", "D"),
            ("D", "R"),
            ("R", "E"),
            ("E", "G"),
            ("E", "F"),
            ("E", "K"),
            ("F", "M"),
            ("F", "O"),
            ("M", "P"),
            ("K", "O"),
            ("P", "C"),
            ("O", "C"),
        ]
        self.draw_lines(edges, self.positions_star)

    # Draw lines between nodes to represent edges
    def draw_lines(self, edges, positions):
        for start, end in edges:
            start_pos = positions[start]
            end_pos = positions[end]

            # Calculate the angle between the two points
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            angle = math.atan2(dy, dx)

            # Adjust start and end points to be on the edge of the circles
            start_x = start_pos[0] + NODE_RADIUS * math.cos(angle)
            start_y = start_pos[1] + NODE_RADIUS * math.sin(angle)
            end_x = end_pos[0] - NODE_RADIUS * math.cos(angle)
            end_y = end_pos[1] - NODE_RADIUS * math.sin(angle)

            line = self.canvas.create_line(start_x, start_y, end_x, end_y, width=3)
            self.node_lines[(start, end)] = line  # Store the line reference

    # Create a circular node on the canvas
    def create_circle(self, x, y, r, node):
        circle = self.canvas.create_oval(
            x - r, y - r, x + r, y + r, outline="black", width=2
        )
        self.canvas.create_text(x, y, text=node, font=FONT)
        return circle

    # Update the color of a node and its connecting line
    def update_node_color(self, node, color, animate=True):
        if node in self.nodes:
            self.logic.node_colors[node] = color
            self.canvas.itemconfig(self.nodes[node], fill=color)

            # Highlight the corresponding node in the list
            if hasattr(self, "node_labels") and node in self.node_labels:
                self.highlight_node_in_list(node, color)

            if animate:
                self.canvas.update()
                time.sleep(TIME_SECONDS)

    # Display a message when the goal node is reached
    def show_goal_message(self, goal_node):
        messagebox.showinfo("Goal Reached", f"Goal node '{goal_node}' reached!")

    # Create the user input interface for root and goal node selection
    def create_input_ui(self, depth_limit=False):
        tk.CTkLabel(self.main_frame, text="Start Node:").grid(
            row=3, column=0, padx=5, pady=5, sticky="e"
        )
        self.start_node_entry = tk.CTkEntry(self.main_frame, width=140)
        self.start_node_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.CTkLabel(self.main_frame, text="Goal Node (Optional):").grid(
            row=4, column=0, padx=5, pady=5, sticky="e"
        )
        self.goal_node_entry = tk.CTkEntry(self.main_frame, width=140)
        self.goal_node_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        self.depth_limit_label = tk.CTkLabel(self.main_frame, text="Depth Limit:")
        self.depth_limit_entry = tk.CTkEntry(self.main_frame, width=140)

        self.start_button = tk.CTkButton(
            self.main_frame, text="Start", command=self.start_function
        )

        self.reset_button = tk.CTkButton(
            self.main_frame,
            text="Reset",
            command=self.reset_function,
            fg_color="red",
            hover_color="darkred",
        )
        # if depth_limit is True:
        #     print("Depth limit is true")
        #     self.depth_limit_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        #     self.depth_limit_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        #     self.start_button.grid(row=6, column=1, pady=5, padx=5, sticky="w")
        #     self.reset_button.grid(row=6, column=0, pady=5, padx=5, sticky="e")
        # else:
        #     print("Depth limit is false")
        #     self.depth_limit_label.grid_forget()
        #     self.depth_limit_entry.grid_forget()
        #     self.start_button.grid_forget()
        #     self.reset_button.grid_forget()
        #     time.sleep(TIME_SECONDS)
        #
        self.start_button.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        self.reset_button.grid(row=5, column=0, pady=5, padx=5, sticky="e")
        self.root.bind("<Return>", lambda event: self.start_function())

    # Reset function to clear the canvas and reset the UI
    def reset_function(self):
        self.clear_canvas()

        uninformed_algorithm = self.selected_uninformed_algorithm.get()
        informed_algorithm = self.selected_informed_algorithm.get()

        # For uninformed algorithms and GBFS
        if uninformed_algorithm != "None" or informed_algorithm == "GBFS":
            self.draw_nodes()
            self.draw_edges()
        # For A* algorithm
        elif informed_algorithm == "A-star":
            self.draw_graph()
            self.display_node_list(self.main_frame, True)

    # Validates the user input and starts the search algorithm
    def start_function(self):
        start_node = self.start_node_entry.get().strip().upper()
        goal_node = self.goal_node_entry.get().strip().upper()

        print("START COUNT: ", TreeVisualizer.start_count)

        if TreeVisualizer.start_count != 0:
            self.reset_cost_display()
            self.logic.reset_colors()

        uninformed_algorithm = self.selected_uninformed_algorithm.get()
        informed_algorithm = self.selected_informed_algorithm.get()

        # Initialize the logic class based on the selected algorithm
        if uninformed_algorithm != "None" and informed_algorithm == "None":

            if start_node not in self.positions_tree.keys():
                messagebox.showerror(
                    "Error", "Invalid start node. Please enter a valid node."
                )
                return

            if uninformed_algorithm == "BFS":
                self.logic.bfs(start_node, goal_node)
            elif uninformed_algorithm == "DFS":
                self.logic.dfs(start_node, goal_node)
            elif uninformed_algorithm == "DLS":
                depth_limit = self.depth_limit_entry.get().strip()
                self.logic.dls(start_node, goal_node, depth_limit)
            elif uninformed_algorithm == "IDS":
                self.logic.ids(start_node, goal_node)
            elif uninformed_algorithm == "UCS":
                self.logic.ucs(start_node, goal_node)

        elif uninformed_algorithm == "None" and informed_algorithm != "None":

            if start_node not in self.positions_star.keys():
                messagebox.showerror(
                    "Error", "Invalid start node. Please enter a valid node."
                )
                return
            if informed_algorithm == "GBFS":
                self.heuristics = heuristics_list.copy()
                if goal_node:
                    self.heuristics[goal_node] = 0
                    self.logic.set_heuristics(self.heuristics)
                    self.update_node_heuristics_display()
                self.logic.greedy_bfs(start_node, goal_node)

            elif informed_algorithm == "A-star":
                self.display_node_list(self.main_frame, True)
                time.sleep(TIME_SECONDS)
                self.draw_graph()
                self.logic.astar(start_node, goal_node)

        else:
            messagebox.showerror(
                "Error",
                "Please select only one algorithm type: either Uninformed or Informed.",
            )

        TreeVisualizer.start_count += 1

    # Update the display of heuristic values for each node
    def update_node_heuristics_display(self):
        for node, (x, y) in self.positions_tree.items():
            if node in self.heuristic_texts:
                self.canvas.delete(self.heuristic_texts[node])
            heuristic_value = self.heuristics.get(node, "")
            self.heuristic_texts[node] = self.canvas.create_text(
                x, y + NODE_RADIUS + 10, text=str(heuristic_value), font=("Arial", 12)
            )

    # Clear all elements from the canvas
    def clear_canvas(self):
        self.canvas.delete("all")

    # Clear the displayed heuristic values from the canvas
    def clear_node_heuristics_display(self):
        for _, text_id in self.heuristic_texts.items():
            self.canvas.delete(text_id)
        self.heuristic_texts.clear()

    # Reset the cost display for all nodes
    def reset_cost_display(self):
        if hasattr(self.logic, "cost_text_ids") and self.logic.cost_text_ids:
            for node in self.nodes:
                if node in self.logic.cost_text_ids:
                    self.canvas.delete(self.logic.cost_text_ids[node])
            self.logic.cost_text_ids.clear()

    # Update Cost dispaly
    def update_cost_display(self, node, cost):
        if node in self.nodes:
            if node in self.logic.cost_text_ids:
                self.canvas.delete(self.logic.cost_text_ids[node])
            x, y = self.positions_tree[node]
            text_id = self.canvas.create_text(
                x, y + NODE_RADIUS + NODE_RADIUS, text=str(cost), font=SMALL_FONT
            )
            self.logic.cost_text_ids[node] = text_id
            self.canvas.itemconfig(self.nodes[node], fill=self.logic.node_colors[node])

    def display_node_list(self, frame, show_list=True):
        if not hasattr(self, "display_frame") or self.display_frame is None:
            self.display_frame = tk.CTkFrame(frame)

        if not show_list:
            self.display_frame.grid_remove()
            return

        self.display_frame.grid(row=0, column=2, rowspan=6, sticky="nsew", padx=10)
        self.node_labels.clear()

        # Title
        title_label = tk.CTkLabel(self.display_frame, text="Node List", font=FONT)
        title_label.grid(row=0, column=0, columnspan=4)

        # Headers
        headers = ["Node", "Place", "Cost", "Distance"]
        widths = [50, 100, 50, 80]

        for col, (header, width) in enumerate(zip(headers, widths)):
            tk.CTkLabel(
                self.display_frame, text=header, font=NORMAL_FONT, width=width
            ).grid(row=1, column=col, padx=5, pady=5)

        # Data rows
        for i, (key, _) in enumerate(self.positions_star.items(), start=2):
            node_letter = key
            name = self.SURIGAO_DEL_NORTE.get(key, "N/A")
            cost = self.SURIGAO_DEL_NORTE_COST.get(key, "N/A")
            distance = self.SURIGAO_DEL_NORTE_DISTANCE.get(key, "N/A")

            # Create row frame
            row_frame = tk.CTkFrame(self.display_frame)
            row_frame.grid(row=i, column=0, columnspan=4, sticky="ew", pady=2)
            self.node_labels[key] = row_frame

            # Node data
            data = [
                node_letter,
                name,
                f"{cost:.2f}" if isinstance(cost, float) else cost,
                f"{distance:.1f} km" if isinstance(distance, float) else distance,
            ]

            for col, (item, width) in enumerate(zip(data, widths)):
                tk.CTkLabel(
                    row_frame,
                    text=item,
                    font=NORMAL_FONT,
                    width=width,
                    text_color="white",
                ).grid(row=0, column=col, padx=5)

    # highlighting nodes in the list
    def highlight_node_in_list(self, node, color):
        if self.current_highlighted and self.current_highlighted in self.node_labels:
            self.node_labels[self.current_highlighted].configure()

        if node in self.node_labels:
            self.current_highlighted = node
            self.node_labels[node].configure(fg_color=color)
            self.node_labels[node].update()

    # Update the position of the legend when the canvas is resized
    def update_legend_position(self, event=None):
        self.canvas.delete("legend")
        self.create_legend()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.CTk()
    visualizer = TreeVisualizer(root)
    visualizer.run()
