# Define constants for colors to be used for marking the status of nodes
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

# Heuristic values for nodes (used in GBFS)
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
SURIGAO_DEL_NORTE_DISTANCE = {
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
        'Surigao City':0,
        'Tagana-an': 23.5,
        'Tubod': 35.2,
        }

SURIGAO_DEL_NORTE_DIRECTION = {
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
        
    # Reset all node colors to 'not visited'
    def reset_colors(self, change = False):
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.node_colors}
        for node in self.node_colors:
            self.update_node_color(node, COLOR_NOT_VISITED, animate=False)  # Instant reset
            
        if change == True:
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

