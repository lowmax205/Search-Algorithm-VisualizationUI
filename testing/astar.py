from queue import PriorityQueue
from source import BaseSearchLogic
import math

class AStarLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.edges = {}
        self.heuristics = {}
        self.positions = {}

    def set_custom_costs_and_heuristics(self):
        self.edges = {
            ('S', 'N'): 10.6, ('S', 'Q'): 15.3, ('S', 'T'): 14.35, ('S', 'E'): 35.67,
            ('N', 'J'): 20.7, ('J', 'I'): 35.5, ('I', 'U'): 6.8, ('U', 'A'): 11.3, 
            ('U', 'L'): 16.3, ('Q', 'U'): 17.0, ('T', 'Q'): 10.0, ('T', 'L'): 9.1,
            ('L', 'B'): 10.7, ('B', 'H'): 14.3, ('H', 'D'): 10.7, ('D', 'R'): 41.1,
            ('R', 'E'): 24.8, ('E', 'G'): 15.2, ('E', 'F'): 22.4, ('E', 'K'): 25.6,
            ('F', 'M'): 11.5, ('F', 'O'): 13.8, ('M', 'P'): 8.4, ('K', 'O'): 11.0,
            ('P', 'C'): 10.1, ('O', 'C'): 11.8
        }

        self.heuristics = {
            'S': 0, 'N': 7.98, 'J': 21.70, 'I': 28.06, 'U': 27.67, 'A': 37.57, 'L': 19.16,
            'Q': 15.30, 'T': 14.35, 'B': 25.95, 'H': 21.20, 'D': 35.67, 'R': 52.22,
            'E': 61.45, 'G': 72.12, 'F': 54.70, 'K': 67.00, 'M': 59.33, 'O': 67.00,
            'P': 64.70, 'C': 68.45
        }

    def astar(self, start_node, goal_node):
        self.set_custom_costs_and_heuristics()  

        open_list = PriorityQueue()
        open_list.put((0, start_node))
        came_from = {}
        g_score = {node: float('inf') for node in self.positions}
        g_score[start_node] = 0

        while not open_list.empty():
            current_f, current_node = open_list.get()

            self.update_node_color(current_node, 'yellow') 
            if current_node == goal_node:
                self.show_goal_message(goal_node)
                self.reconstruct_path(came_from, start_node, goal_node)
                return

            self.update_node_color(current_node, 'green') 

            for neighbor, cost in self.get_neighbors(current_node):
                tentative_g_score = g_score[current_node] + cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = g_score[neighbor] + self.heuristics.get(neighbor, float('inf'))
                    open_list.put((f_score, neighbor))

        return None

    def get_neighbors(self, node):
        neighbors = []
        for (start, end), cost in self.edges.items():
            if start == node:
                neighbors.append((end, cost))
            elif end == node:
                neighbors.append((start, cost))
        return neighbors

    def reconstruct_path(self, came_from, start_node, goal_node):
        current = goal_node
        while current in came_from:
            current = came_from[current]
            self.update_node_color(current, 'blue', animate=True)

# Path	Cost	   	Heuristic

# S>N	10.6		0	    7.98
# S>Q	15.30		0	    19.3
# S>T	14.35		0	    22.5
# S>E	35.67		0	    65.2
# N>J	20.7		7.98	21.70
# J>I	35.5		21.70	28.06
# I>U 	6.8		    28.06	27.67
# U>A	11.3		27.67	37.57
# U>L	16.3		27.67	19.16
# Q>U	17.0		15.30	27.67
# T>Q	10.0		14.35	15.30
# T>L 	9.1		    14.35	19.16
# L>B	10.7		19.16	25.95
# B>H	14.3		25.95	21.20
# H>D	10.7		21.20	35.67
# D>R	41.1		35.67	52.22
# R>E	24.8		52.22	61.45
# E>G	15.2		61.45	72.12
# E>F	22.4		61.45	54.70
# E>K	25.6		61.45	67.00
# F>M	11.5		54.70	59.33
# F>O	13.8		54.70	67.00
# M>P	8.4		    59.33	64.70
# K>O	11.0		67.00	67.00
# P>C	10.1		64.70	68.45
# O>C	11.8		67.00	68.45