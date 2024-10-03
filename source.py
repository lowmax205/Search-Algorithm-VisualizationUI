# Define constants for colors to be used for marking the status of nodes
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

# Heuristic values for nodes (used in GBFS, A-star, etc.)
ORIGINAL_HEURISTICS = {
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

class BaseSearchLogic:
    # Initialize with canvas, functions to update node color and show goal message
    def __init__(self, canvas, update_node_color, show_goal_message):
        self.canvas = canvas  
        self.update_node_color = update_node_color 
        self.show_goal_message = show_goal_message 
        self.node_colors = {}  
        self.node_costs = {}
        self.cost_text_ids = {}

    # Set positions for nodes and initialize their colors to 'not visited'
    def set_positions(self, positions):
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}

    def reset_colors(self):
        # Reset all node colors to 'not visited' instantly
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.node_colors}
        for node in self.node_colors:
            self.update_node_color(node, COLOR_NOT_VISITED, animate=False)  # Instant reset
        print("All nodes have been reset to 'not visited'.")


    # Return neighbors for a given node (used for search algorithms)
    def get_neighbors(self, node):
        neighbors = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': ['H', 'I'],
            'E': [],
            'F': ['J', 'K'],
            'G': [],
            'H': ['L'],
            'I': ['M'],
            'J': ['N'],
            'K': [],
            'L': [],
            'M': [],
            'N': []
        }
        return neighbors.get(node, []) 
    
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
