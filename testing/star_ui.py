import tkinter as tk
from tkinter import Canvas
import math
import time
from astar import AStarLogic

FONT = ('Arial', 14, 'bold')
NORMAL_FONT = ('Arial', 12)
NODE_RADIUS = 20
time_seconds = 0.2

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Layout")
        self.canvas = Canvas(root, width=1000, height=900, bg="white")
        self.canvas.pack(side=tk.LEFT)

        self.positions = {
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
        
        self.SURIGAO_DEL_NORTE_DISTANCE = {
                'A': 46.3,
                'B': 38.7,
                'C': 104,
                'D': 55.1,
                'E': 65.2,
                'F': 87.3,
                'G': 80.4,
                'H': 52.7,
                'I': 36.1,
                'J': 30.9,
                'K': 90.70,
                'L': 31.8, 
                'M': 94.2,
                'N': 10.6,
                'O': 93.5,
                'P': 102,
                'Q': 19.3,
                'R': 95.7,
                'S':0,
                'T': 23.5,
                'U': 35.2,
                }

        self.SURIGAO_DEL_NORTE_COST = {
            'A': 37.57,
            'B': 25.95,
            'C': 68.45,
            'D': 35.67,
            'E': 61.45,
            'F': 54.70,
            'G': 72.12,
            'H': 21.20,
            'I': 28.06,
            'J': 21.70,
            'K': 67.00,
            'L': 19.16,
            'M': 59.33,
            'N': 7.98,
            'O': 67.00,
            'P': 64.70,
            'Q': 15.30,
            'R': 52.22,
            'S': 0,
            'T': 14.35,
            'U': 27.67
        }
                
        self.SURIGAO_DEL_NORTE = {
            'A': 'Alegria',
            'B': 'Bacuag',
            'C': 'Burgos',
            'D': 'Claver',
            'E': 'Dapa',
            'F': 'Del Carmen',
            'G': 'General Luna',
            'H': 'Gigaquit',
            'I': 'Mainit',
            'J': 'Malimono',
            'K': 'Pilar',
            'L': 'Placer',
            'M': 'San Benito',
            'N': 'San Francisco',
            'O': 'San Isidro',
            'P': 'Santa Monica',
            'Q': 'Sison',
            'R': 'Socorro',
            'S': 'Surigao City',
            'T': 'Tagana-an',
            'U': 'Tubod'
        }

        self.nodes = {}
        self.logic = AStarLogic(self.canvas, self.update_node_color, self.show_goal_message)
        self.logic.set_positions(self.positions)

        self.draw_graph()

        frame = tk.Frame(root)
        frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.start_label = tk.Label(frame, text="Start Node:", font=FONT)
        self.start_label.pack()
        self.start_entry = tk.Entry(frame)
        self.start_entry.pack()

        self.goal_label = tk.Label(frame, text="Goal Node:", font=FONT)
        self.goal_label.pack()
        self.goal_entry = tk.Entry(frame)
        self.goal_entry.pack()

        self.search_button = tk.Button(frame, text="Start A* Search", command=self.start_search)
        self.search_button.pack()

        self.display_node_list(frame)
    
    def display_node_list(self, frame):
        label = tk.Label(frame, text="Node List", font=FONT)
        label.pack()
        subt = tk.Label(frame, text="Place              Cost               Distance", font=NORMAL_FONT)
        subt.pack()

        # Loop through positions to display node informatio
        for node in self.positions.keys():
            name = self.SURIGAO_DEL_NORTE.get(node, "N/A")
            cost = self.SURIGAO_DEL_NORTE_COST.get(node, "N/A")
            distance = self.SURIGAO_DEL_NORTE_DISTANCE.get(node, "N/A")

            lbl = tk.Label(frame, text=f"{name}         -           {cost}          -       {distance} km")
            lbl.pack()

    def start_search(self):
        start_node = self.start_entry.get().strip().upper()
        goal_node = self.goal_entry.get().strip().upper()

        if start_node in self.positions and goal_node in self.positions:
            self.logic.reset_colors()
            self.logic.astar(start_node, goal_node)
        else:
            print("Invalid start or goal node.")

    def draw_graph(self):
        self.draw_nodes()
        self.draw_edges()

    def draw_nodes(self):
        for node, (x, y) in self.positions.items():
            self.nodes[node] = self.create_circle(x, y, NODE_RADIUS, node)

    def draw_edges(self):
        for start, end in self.edges:
            self.create_line(*self.positions[start], *self.positions[end], NODE_RADIUS)

    def create_circle(self, x, y, r, node):
        circle = self.canvas.create_oval(x - r, y - r, x + r, y + r, outline="black", width=2, fill="white")
        self.canvas.create_text(x, y, text=node, font=FONT)
        return circle

    def create_line(self, x1, y1, x2, y2, r):
        angle = math.atan2(y2 - y1, x2 - x1)
        start_x = x1 + r * math.cos(angle)
        start_y = y1 + r * math.sin(angle)
        end_x = x2 - r * math.cos(angle)
        end_y = y2 - r * math.sin(angle)
        self.canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST, width=2)

    def update_node_color(self, node, color, animate=True):
        if node in self.nodes:
            self.logic.node_colors[node] = color
            self.canvas.itemconfig(self.nodes[node], fill=color)
            if animate:
                self.root.update()
                time.sleep(time_seconds)

    def show_goal_message(self, goal_node):
        print(f"Goal {goal_node} reached!")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
