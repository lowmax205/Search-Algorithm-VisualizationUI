import math
# Define constants for colors to be used for marking the status of nodes
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class BaseSearchLogic:
    # Initialize with canvas, functions to update node color and show goal message
    def __init__(self, canvas, update_node_color, show_goal_message):
        self.canvas = canvas  
        self.update_node_color = update_node_color 
        self.show_goal_message = show_goal_message 
        self.node_colors = {}  

    # Set positions for nodes and initialize their colors to 'not visited'
    def set_positions(self, positions):
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}
        
    # Reset all node colors to 'not visited'
    def reset_colors(self, change = False):
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.node_colors}
        for node in self.node_colors:
            self.update_node_color(node, COLOR_NOT_VISITED, animate=False)  # Instant reset
            
        if change == True:
            print("All nodes have been reset to 'not visited'.")
            
    # Return neighbors with associated costs for UCS (Uniform Cost Search)
    def ucs_get_neighbors(self, node):
        neighbors_with_costs = {
            'A': [('B', 1), ('C', 2)],
            'B': [('D', 4), ('E', 2)],
            'C': [('F', 3), ('G', 2)],
            'D': [('H', 7), ('I', 3)],
            'E': [],
            'F': [('J', 5), ('K', 4)],
            'G': [],
            'H': [('L', 6)],
            'I': [('M', 3)],
            'J': [('N', 2)],
            'K': [],
            'L': [],
            'M': [],
            'N': []
        }
        return neighbors_with_costs.get(node, [])