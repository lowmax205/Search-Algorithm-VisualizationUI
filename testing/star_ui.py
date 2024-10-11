import customtkinter as ctk  # Use CustomTkinter instead of tkinter
from tkinter import Canvas, messagebox
import math
import time
from astar import AStarLogic

# Set the appearance mode and color theme (optional)
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

FONT = ('Arial', 14, 'bold')
NORMAL_FONT = ('Arial', 12)
NODE_RADIUS = 20
time_seconds = 0.2

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Layout")
        self.root.minsize(1200, 900)

        # Create frames for layout
        self.left_frame = ctk.CTkFrame(root)
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH)

        self.right_frame = ctk.CTkFrame(root)
        self.right_frame.pack(side=ctk.RIGHT, fill=ctk.Y)

        # Canvas for drawing the graph
        self.canvas = Canvas(self.left_frame, width=1000, height=300, bg="white")
        self.canvas.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        # Bottom frame for input widgets
        self.bottom_frame = ctk.CTkFrame(root)
        self.bottom_frame.place(relx=0.5, rely=0.9, anchor='center')

        # Initialize positions and edges
        self.init_graph_data()
        
        # Setup A* Logic
        self.nodes = {}
        self.logic = AStarLogic(self.canvas, self.update_node_color, self.show_goal_message)
        self.logic.set_positions(self.positions_star)

        self.draw_graph()
        self.create_widgets(self.bottom_frame)
        self.display_node_list(self.right_frame)

    def init_graph_data(self):
        # Graph data
        self.positions_star = {
            'A': (350, 800), 'B': (600, 700), 'C': (850, 50), 'D': (700, 800),
            'E': (700, 400), 'F': (750, 300), 'G': (900, 400), 'H': (650, 750),
            'I': (250, 650), 'J': (150, 600), 'K': (900, 300), 'L': (500, 650),
            'M': (650, 250), 'N': (100, 450), 'O': (900, 200), 'P': (750, 150),
            'Q': (300, 500), 'R': (700, 600), 'S': (300, 400), 'T': (500, 500),
            'U': (400, 600)
        }

        self.edges = [
            ('S', 'N'), ('S','Q'), ('S', 'T'), ('S', 'E'),
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

        # Distance and cost data
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

    def create_widgets(self, frame):
        # Widgets for input using CustomTkinter
        self.start_label = ctk.CTkLabel(frame, text="Start Node:", font=FONT)
        self.start_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.start_entry = ctk.CTkEntry(frame)
        self.start_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.goal_label = ctk.CTkLabel(frame, text="Goal Node:", font=FONT)
        self.goal_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.goal_entry = ctk.CTkEntry(frame)
        self.goal_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.search_button = ctk.CTkButton(frame, text="Start A* Search", command=self.start_search)
        self.search_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='w')

    def display_node_list(self, frame):
        # Node list in right frame
        label = ctk.CTkLabel(frame, text="Node List", font=FONT)
        label.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky='we')

        # Sub-headings for node information
        subt_node = ctk.CTkLabel(frame, text="Node", font=NORMAL_FONT)
        subt_node.grid(row=1, column=0, padx=5, sticky='w')

        subt_place = ctk.CTkLabel(frame, text="Place", font=NORMAL_FONT)
        subt_place.grid(row=1, column=1, padx=5, sticky='w')

        subt_cost = ctk.CTkLabel(frame, text="Cost", font=NORMAL_FONT)
        subt_cost.grid(row=1, column=2, padx=5, sticky='w')

        subt_distance = ctk.CTkLabel(frame, text="Distance", font=NORMAL_FONT)
        subt_distance.grid(row=1, column=3, padx=5, sticky='w')

        # Loop through positions to display node information
        for i, (key, _) in enumerate(self.positions_star.items(), start=2):
            node_letter = key
            name = self.SURIGAO_DEL_NORTE.get(key, "N/A")
            cost = self.SURIGAO_DEL_NORTE_COST.get(key, "N/A")
            distance = self.SURIGAO_DEL_NORTE_DISTANCE.get(key, "N/A")

            lbl_node = ctk.CTkLabel(frame, font=('Arial', 10), text=node_letter)
            lbl_node.grid(row=i, column=0, padx=5, sticky='w')

            lbl_name = ctk.CTkLabel(frame, font=('Arial', 10), text=name)
            lbl_name.grid(row=i, column=1, padx=5, sticky='w')

            lbl_cost = ctk.CTkLabel(frame, font=('Arial', 10), text=cost)
            lbl_cost.grid(row=i, column=2, padx=5, sticky='w')

            lbl_distance = ctk.CTkLabel(frame, font=('Arial', 10), text=f"{distance} km")
            lbl_distance.grid(row=i, column=3, padx=5, sticky='w')

    def draw_graph(self):
        # Draw nodes
        for node, (x, y) in self.positions_star.items():
            self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill="lightblue")
            self.canvas.create_text(x, y, text=node, font=NORMAL_FONT)

        # Draw edges
        for start, end in self.edges:
            x1, y1 = self.positions_star[start]
            x2, y2 = self.positions_star[end]
            self.canvas.create_line(x1, y1, x2, y2, fill="black")

    def update_node_color(self, node, color):
        x, y = self.positions_star[node]
        self.canvas.create_oval(x - NODE_RADIUS, y - NODE_RADIUS, x + NODE_RADIUS, y + NODE_RADIUS, fill=color)


    def show_goal_message(self):
        messagebox.showinfo("Goal Found", "The A* Search has reached the goal!")

    def start_search(self):
        start_node = self.start_entry.get().strip().upper()  # Ensure upper case
        goal_node = self.goal_entry.get().strip().upper()    # Ensure upper case

        if start_node not in self.positions_star or goal_node not in self.positions_star:
            messagebox.showerror("Invalid Input", "Please enter valid node names.")
            return

        self.logic.astar(start_node, goal_node)


if __name__ == "__main__":
    root = ctk.CTk()  # Use CustomTkinter root window
    app = GraphApp(root)
    root.mainloop()
