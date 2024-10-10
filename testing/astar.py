from queue import PriorityQueue  
from source import BaseSearchLogic

# Color constants
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'
COLOR_PATH = 'blue'

class AStarLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message):
        # Initialize the base class and set up necessary variables for the A* algorithm
        super().__init__(canvas, update_node_color, show_goal_message)
        self.edges = {}
        self.heuristics = {}
        self.positions = {}

    def set_custom_costs_and_heuristics(self):
        # Set path costs for each connection between nodes (edges)
        self.edges = {
            ('S', 'N'): 10.6, ('S', 'Q'): 15.3, ('S', 'T'): 14.35, ('S', 'E'): 35.67,
            ('N', 'J'): 20.7, ('J', 'I'): 35.5, ('I', 'U'): 6.8, ('U', 'A'): 11.3, 
            ('U', 'L'): 16.3, ('Q', 'U'): 17.0, ('T', 'Q'): 10.0, ('T', 'L'): 9.1,
            ('L', 'B'): 10.7, ('B', 'H'): 14.3, ('H', 'D'): 10.7, ('D', 'R'): 41.1,
            ('R', 'E'): 24.8, ('E', 'G'): 15.2, ('E', 'F'): 22.4, ('E', 'K'): 25.6,
            ('F', 'M'): 11.5, ('F', 'O'): 13.8, ('M', 'P'): 8.4, ('K', 'O'): 11.0,
            ('P', 'C'): 10.1, ('O', 'C'): 11.8
        }

        # Set heuristic values for each node (the estimated distance to the goal)
        self.heuristics = {
            'S': 0, 'N': 7.98, 'J': 21.70, 'I': 28.06, 'U': 27.67, 'A': 37.57, 'L': 19.16,
            'Q': 15.30, 'T': 14.35, 'B': 25.95, 'H': 21.20, 'D': 35.67, 'R': 52.22,
            'E': 61.45, 'G': 72.12, 'F': 54.70, 'K': 67.00, 'M': 59.33, 'O': 67.00,
            'P': 64.70, 'C': 68.45
        }
    # A* algorithm implementation to find the shortest path from start_node to goal_node
    def astar(self, start_node, goal_node):

        self.set_custom_costs_and_heuristics()

        # Initialize the open list (PriorityQueue) to store nodes to explore, starting with the start_node
        open_list = PriorityQueue()
        open_list.put((0, start_node))
        came_from = {}
        g_score = {node: float('inf') for node in self.positions}
        g_score[start_node] = 0 
        index = 0
        while not open_list.empty():
            current_f, current_node = open_list.get() 

            # Update the visualization: Mark the current node as visiting
            self.update_node_color(current_node, COLOR_VISITING)
            
            # If the goal node is reached, reconstruct the path and exit
            if current_node == goal_node:
                self.reconstruct_path(came_from, start_node, goal_node)
                self.show_goal_message(goal_node)
                return

            self.update_node_color(current_node, COLOR_VISITED)

            
            # Explore neighbors of the current node
            for neighbor, cost in self.get_neighbors(current_node):
                index += 1
                tentative_g_score = g_score[current_node] + cost
                print(f"Current node{index} = {g_score[current_node]} + {cost} = {tentative_g_score}")
                # If this path is better (lower g_score), update came_from and the scores
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = g_score[neighbor] + self.heuristics.get(neighbor, float('inf'))
                    open_list.put((f_score, neighbor))

        return None
    
    # Helper function to get all neighbors of the current node and their path costs
    def get_neighbors(self, node):
        neighbors = []
        # If the current node is either the start or end of an edge, it's a neighbor
        for (start, end), cost in self.edges.items():
            if start == node:
                neighbors.append((end, cost))
            elif end == node:
                neighbors.append((start, cost))
        return neighbors
    
    # Reconstruct and visualize the path from start_node to goal_node using came_from dictionary
    def reconstruct_path(self, came_from, start_node, goal_node):
        current = goal_node
        path = []
        path.append(goal_node)

        while current in came_from:
            current = came_from[current]
            path.append(current)
            self.update_node_color(current, COLOR_PATH, animate=True)

        path.reverse()
        
        print("Path:", " -> ".join(path))
        print(f"-> Goal: {goal_node}")
