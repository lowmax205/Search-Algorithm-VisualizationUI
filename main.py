import customtkinter as tk
import time
import math
from tkinter import messagebox
from source import ORIGINAL_HEURISTICS as heuristics_list

from uninformed.bfs import BFSLogic
from uninformed.dfs import DFSLogic
from uninformed.dls import DFS_DLSLogic
from uninformed.ids import IDSLogic
from uninformed.ucs import UCSLogic

from informed.gbfs import GBFSLogic
from informed.astar import AStarLogic

FONT = ('Arial', 14, 'bold')
NORMAL_FONT = ('Arial', 12)
SMALL_FONT = ('Arial', 10)
NODE_RADIUS = 20
time_seconds = 0.1

class TreeVisualizer:
    start_count = 0
    # Constructor for initializing the main window and its components
    def __init__(self, root):
        self.root = root
        self.root.title("Search Algorithm Visualization")

        tk.set_appearance_mode("dark")
        tk.set_default_color_theme("dark-blue")
        
        self.main_frame = tk.CTkFrame(self.root)
        self.main_frame.pack(pady=10)

        self.canvas = tk.CTkCanvas(self.main_frame, width=600, height=500)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.positions_tree = {
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
        
        scale_x = 400 / 500
        scale_y = 300 / 500
        self.positions_star = {
        'A': (int(350 * scale_x), int(800 * scale_y)),
        'B': (int(600 * scale_x), int(700 * scale_y)),
        'C': (int(850 * scale_x), int(50 * scale_y)),
        'D': (int(700 * scale_x), int(800 * scale_y)),
        'E': (int(700 * scale_x), int(400 * scale_y)),
        'F': (int(750 * scale_x), int(300 * scale_y)),
        'G': (int(900 * scale_x), int(400 * scale_y)),
        'H': (int(650 * scale_x), int(750 * scale_y)),
        'I': (int(250 * scale_x), int(650 * scale_y)),
        'J': (int(150 * scale_x), int(600 * scale_y)),
        'K': (int(900 * scale_x), int(300 * scale_y)),
        'L': (int(500 * scale_x), int(650 * scale_y)),
        'M': (int(650 * scale_x), int(250 * scale_y)),
        'N': (int(100 * scale_x), int(450 * scale_y)),
        'O': (int(900 * scale_x), int(200 * scale_y)),
        'P': (int(750 * scale_x), int(150 * scale_y)),
        'Q': (int(300 * scale_x), int(500 * scale_y)),
        'R': (int(700 * scale_x), int(600 * scale_y)),
        'S': (int(300 * scale_x), int(400 * scale_y)),
        'T': (int(500 * scale_x), int(500 * scale_y)),
        'U': (int(400 * scale_x), int(600 * scale_y)),
    }

        self.heuristics = heuristics_list.copy()
        self.heuristic_texts = {} 
        self.nodes = {} 
        self.edges = []
        
        self.selected_uninformed_algorithm = tk.StringVar()  
        self.selected_uninformed_algorithm.set("None")  
        self.selected_informed_algorithm = tk.StringVar()
        self.selected_informed_algorithm.set("None") 

        tk.CTkLabel(self.main_frame, text="Select Uninformed Algorithm:").grid(row=1, column=0, padx=5, pady=5)
        uninformed_menu = tk.CTkOptionMenu(
            self.main_frame,
            variable=self.selected_uninformed_algorithm, 
            values=["None", "BFS", "DFS", "DLS", "IDS", "UCS"], 
            command=self.update_algorithm)
        uninformed_menu.grid(row=1, column=1, padx=5, pady=5)

        tk.CTkLabel(self.main_frame, text="Select Informed Algorithm:").grid(row=2, column=0, padx=5, pady=5)
        informed_menu = tk.CTkOptionMenu(
            self.main_frame, 
            variable=self.selected_informed_algorithm, 
            values=["None", "GBFS", "A-star"], 
            command=self.update_algorithm)
        informed_menu.grid(row=2, column=1, padx=5, pady=5)

        self.logic = None
        self.update_algorithm("BFS")
        self.draw_nodes()
        self.draw_edges()
        self.create_input_ui()
        
    # Initializes data specific to the graph, such as positions and edges for A star Search
        self.SURIGAO_DEL_NORTE_DISTANCE = {
            'A': 46.3, 'B': 38.7, 'C': 104, 'D': 55.1, 'E': 65.2, 
            'F': 87.3, 'G': 80.4, 'H': 52.7, 'I': 36.1, 'J': 30.9, 
            'K': 90.70, 'L': 31.8, 'M': 94.2, 'N': 10.6, 'O': 93.5, 
            'P': 102, 'Q': 19.3, 'R': 95.7, 'S': 0, 'T': 23.5, 'U': 35.2
        }

        self.SURIGAO_DEL_NORTE_COST = {
            'A': 37.57, 'B': 25.95, 'C': 68.45, 'D': 35.67, 'E': 61.45, 
            'F': 54.70, 'G': 72.12, 'H': 21.20, 'I': 28.06, 'J': 21.70, 
            'K': 67.00, 'L': 19.16, 'M': 59.33, 'N': 7.98, 'O': 67.00, 
            'P': 64.70, 'Q': 15.30, 'R': 52.22, 'S': 0, 'T': 14.35, 'U': 27.67
        }

        self.SURIGAO_DEL_NORTE = {
            'A': 'Alegria', 'B': 'Bacuag', 'C': 'Burgos', 'D': 'Claver', 
            'E': 'Dapa', 'F': 'Del Carmen', 'G': 'General Luna', 
            'H': 'Gigaquit', 'I': 'Mainit', 'J': 'Malimono', 
            'K': 'Pilar', 'L': 'Placer', 'M': 'San Benito', 
            'N': 'San Francisco', 'O': 'San Isidro', 'P': 'Santa Monica', 
            'Q': 'Sison', 'R': 'Socorro', 'S': 'Surigao City', 
            'T': 'Tagana-an', 'U': 'Tubod'
        }
        
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
        elif algorithm_name == 'A-star':
            self.set_algorithm_logic(AStarLogic)
            self.draw_graph()
        elif algorithm_name == "GBFS":
            self.set_algorithm_logic(GBFSLogic, clear_heuristics=False)
            self.logic.set_heuristics(self.heuristics)
            self.update_node_heuristics_display()

        if algorithm_name != 'A-star':
            self.display_node_list(self.main_frame, False)

    def set_algorithm_logic(self, LogicClass, clear_heuristics=True):
        self.clear_canvas()
        if clear_heuristics:
            self.clear_node_heuristics_display()

        if LogicClass == UCSLogic:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message,
                update_cost_display=self.update_cost_display
            )
            self.canvas.config(width=600, height=500)
            
            self.draw_nodes()
            self.draw_edges()

        elif LogicClass == AStarLogic:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message
            )
            self.canvas.config(width=1200, height=700)
            self.draw_graph()
            self.display_node_list(self.main_frame, True)

        else:
            self.logic = LogicClass(
                canvas=self.canvas,
                update_node_color=self.update_node_color,
                show_goal_message=self.show_goal_message
            )
            self.canvas.config(width=600, height=500)
            self.clear_canvas()
            self.draw_nodes()
            self.draw_edges()
        
    # Draws nodes on the canvas
    def draw_nodes(self):
        for node, (x, y) in self.positions_tree.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

    # Creates the edges of the tree and draws them on the canvas
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
            self.create_line(*self.positions_tree[start], *self.positions_tree[end], NODE_RADIUS)

    def create_circle(self, x, y, r, node):
        circle = self.canvas.create_oval(x - r, y - r, x + r, y + r,outline="black", width=2)
        self.canvas.create_text(x, y, text=node, font=FONT)
        return circle

    def create_line(self, x1, y1, x2, y2, r):
        angle = math.atan2(y2 - y1, x2 - x1)
        start_x = x1 + r * math.cos(angle)
        start_y = y1 + r * math.sin(angle)
        end_x = x2 - r * math.cos(angle)
        end_y = y2 - r * math.sin(angle)
        line = self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=2)
        self.edges.append(line)
        
    def draw_graph(self):
        for node, (x, y) in self.positions_star.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

        self.edges = [
            ('S', 'N'), ('S', 'Q'), ('S', 'T'), ('S', 'E'),
            ('N', 'J'), 
            ('J', 'I'), 
            ('I', 'U'), 
            ('U', 'A'), ('U', 'L'),
            ('Q', 'U'), 
            ('T', 'Q'), ('T', 'L'), 
            ('L', 'B'), 
            ('B', 'H'),
            ('H', 'D'), 
            ('D', 'R'), 
            ('R', 'E'), 
            ('E', 'G'), ('E', 'F'), ('E', 'K'), 
            ('F', 'M'), ('F', 'O'), 
            ('M', 'P'), 
            ('K', 'O'),
            ('P', 'C'), 
            ('O', 'C')
        ]

        for start, end in self.edges:
            start_pos = self.positions_star[start]
            end_pos = self.positions_star[end]
            self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], width=2)

    def update_node_color(self, node, color, animate=True):
        if node in self.nodes:
            self.logic.node_colors[node] = color
            self.canvas.itemconfig(self.nodes[node], fill=color)
            if animate:
                self.canvas.update()  # Force update of the canvas
                time.sleep(time_seconds)

    def show_goal_message(self, goal_node):
        messagebox.showinfo("Goal Reached", f"Goal node '{goal_node}' reached!")

    # Create the user input interface for root and goal node selection
    def create_input_ui(self):
        tk.CTkLabel(self.main_frame, text="Start Node:").grid(row=3, column=0, padx=5, pady=5)
        self.start_node_entry = tk.CTkEntry(self.main_frame, width=140)
        self.start_node_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.CTkLabel(self.main_frame, text="Goal Node (Optional):").grid(row=4, column=0, padx=5, pady=5)
        self.goal_node_entry = tk.CTkEntry(self.main_frame, width=140)
        self.goal_node_entry.grid(row=4, column=1, padx=5, pady=5)

        self.start_button = tk.CTkButton(self.main_frame, text="Start", command=self.start_function)
        self.start_button.grid(row=5, column=0, columnspan=2, pady=10)
        
    def validate_input(self, node):
        valid_nodes = set(self.positions_tree.keys())
        return node in valid_nodes
    
    # Validates the user input and starts the search algorithm
    def start_function(self):
        start_node = self.start_node_entry.get().strip().upper()
        goal_node = self.goal_node_entry.get().strip().upper()

        print("START COUNT: ", TreeVisualizer.start_count)
        
        if TreeVisualizer.start_count != 0:
            self.reset_cost_display()
            self.logic.reset_colors()
        
        # if start_node not in self.positions_tree or self.positions_star:
        #     messagebox.showerror("Error", "Invalid start node. Please enter a valid node.")
        #     return

        # if goal_node and not self.validate_input(goal_node):
        #     messagebox.showerror("Error", "Invalid goal node. Please enter a valid node or leave blank.")
        #     return
        
        uninformed_algorithm = self.selected_uninformed_algorithm.get()
        informed_algorithm = self.selected_informed_algorithm.get()
        
        # Initialize the logic class based on the selected algorithm
        if uninformed_algorithm != "None" and informed_algorithm == "None":
        
            
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
            if informed_algorithm == "GBFS":
                self.heuristics = heuristics_list.copy()
                if goal_node:
                    self.heuristics[goal_node] = 0
                    self.logic.set_heuristics(self.heuristics)
                    self.update_node_heuristics_display()
                self.logic.greedy_bfs(start_node, goal_node)
                
            elif informed_algorithm == "A-star":
                self.draw_graph()
                self.logic.astar(start_node, goal_node)

        else:
            messagebox.showerror("Error", "Please select only one algorithm type: either Uninformed or Informed.")

        TreeVisualizer.start_count += 1

    def update_node_heuristics_display(self):
        for node, (x, y) in self.positions_tree.items():
            if node in self.heuristic_texts:
                self.canvas.delete(self.heuristic_texts[node])
            heuristic_value = self.heuristics.get(node, "")
            self.heuristic_texts[node] = self.canvas.create_text(
                x, y + NODE_RADIUS + 10, text=str(heuristic_value), font=('Arial', 12)
            )
    def clear_canvas(self):
        self.canvas.delete("all")
    
    def clear_node_heuristics_display(self):
        for _, text_id in self.heuristic_texts.items():
            self.canvas.delete(text_id)
        self.heuristic_texts.clear()
        
    def reset_cost_display(self):
        if hasattr(self.logic, 'cost_text_ids') and self.logic.cost_text_ids:
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
            text_id = self.canvas.create_text(x, y + NODE_RADIUS + NODE_RADIUS, text=str(cost), font=SMALL_FONT)
            self.logic.cost_text_ids[node] = text_id
            self.canvas.itemconfig(self.nodes[node], fill=self.logic.node_colors[node])

    def display_node_list(self, frame, show_list=True):
        if not hasattr(self, 'display_frame') or self.display_frame is None:
            self.display_frame = tk.CTkFrame(frame, width=100, height=500)
        
        if not show_list:
            self.display_frame.grid_remove()
            return 

        self.display_frame.grid(row=0, column=1, sticky='e')

        for widget in self.display_frame.winfo_children():
            widget.destroy()

        label = tk.CTkLabel(self.display_frame, text="Node List", font=FONT)
        label.grid(row=0, column=0, sticky='we')

        subt_node = tk.CTkLabel(self.display_frame, text="Node", font=NORMAL_FONT)
        subt_node.grid(row=1, column=0, padx=5, sticky='w')

        subt_place = tk.CTkLabel(self.display_frame, text="Place", font=NORMAL_FONT)
        subt_place.grid(row=1, column=1, padx=5, sticky='w')

        subt_cost = tk.CTkLabel(self.display_frame, text="Cost", font=NORMAL_FONT)
        subt_cost.grid(row=1, column=2, padx=5, sticky='w')

        subt_distance = tk.CTkLabel(self.display_frame, text="Distance", font=NORMAL_FONT)
        subt_distance.grid(row=1, column=3, padx=5, sticky='w')

        for i, (key, _) in enumerate(self.positions_star.items(), start=2):
            node_letter = key
            name = self.SURIGAO_DEL_NORTE.get(key, "N/A")
            cost = self.SURIGAO_DEL_NORTE_COST.get(key, "N/A")
            distance = self.SURIGAO_DEL_NORTE_DISTANCE.get(key, "N/A")

            lbl_node = tk.CTkLabel(self.display_frame, font=SMALL_FONT, text=node_letter)
            lbl_node.grid(row=i, column=0, padx=5, sticky='w')

            lbl_name = tk.CTkLabel(self.display_frame, font=SMALL_FONT, text=name)
            lbl_name.grid(row=i, column=1, padx=5, sticky='w')

            lbl_cost = tk.CTkLabel(self.display_frame, font=SMALL_FONT, text=cost)
            lbl_cost.grid(row=i, column=2, padx=5, sticky='w')

            lbl_distance = tk.CTkLabel(self.display_frame, font=SMALL_FONT, text=f"{distance} km")
            lbl_distance.grid(row=i, column=3, padx=5, sticky='w')

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.CTk() 
    visualizer = TreeVisualizer(root) 
    visualizer.run() 