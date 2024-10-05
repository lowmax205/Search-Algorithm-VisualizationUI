import tkinter as tk
from tkinter import Canvas
import math
import time
from astar import AStarLogic

FONT = ('Arial', 14, 'bold')
NORMAL_FONT = ('Arial', 12)
NODE_RADIUS = 20
time_seconds = 0.2

COLOR_VISITING = "yellow"
COLOR_GOAL = "green"
COLOR_VISITED = "blue"

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
            'Alegria': 46.3,
            'Bacuag': 38.7,
            'Burgos': 104,
            'Claver': 55.1,
            'Dapa': 65.2,
            'Del Carmen': 87.3,
            'General Luna': 80.4,
            'Gigaquit': 52.7,
            'Mainit': 36.1,
            'Malimono': 30.9,
            'Pilar': 90.70,
            'Placer': 31.8, 
            'San Benito': 94.2,
            'San Francisco': 10.6,
            'San Isidro': 93.5,
            'Santa Monica': 102,
            'Sison': 19.3,
            'Socorro': 95.7,
            'Surigao City': 0,
            'Tagana-an': 23.5,
            'Tubod': 35.2,
        }

        self.SURIGAO_DEL_NORTE_DIRECTION = {
            'Alegria': 37.57,
            'Bacuag': 25.95,
            'Burgos': 68.45,
            'Claver': 35.67,
            'Dapa': 61.45,
            'Del Carmen': 54.70,
            'General Luna': 72.12,
            'Gigaquit': 21.20,
            'Mainit': 28.06,
            'Malimono': 21.70,
            'Pilar': 67.00,
            'Placer': 19.16,
            'San Benito': 59.33,
            'San Francisco': 7.98,
            'San Isidro': 67.00,
            'Santa Monica': 64.70,
            'Sison': 15.30,
            'Socorro': 52.22,
            'Surigao City': 0,
            'Tagana-an': 14.35,
            'Tubod': 27.67,
        }

        self.nodes = {}
        self.draw_graph()

        frame = tk.Frame(root)
        frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.display_node_list(frame)

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

    def display_node_list(self, frame):
        label = tk.Label(frame, text="Node List", font=FONT)
        label.pack()
        for node in self.positions.keys():
            cost = self.SURIGAO_DEL_NORTE_DIRECTION.get(node, "N/A")
            distance = self.SURIGAO_DEL_NORTE_DISTANCE.get(node, "N/A")
            lbl = tk.Label(frame, text=f"{node} - Cost: {cost} - Distance: {distance} km", font=NORMAL_FONT)
            lbl.pack()

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
