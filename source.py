# Define constants for colors
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class BaseSearchLogic:
    def __init__(self, canvas, update_node_color, show_goal_message):
        self.canvas = canvas
        self.update_node_color = update_node_color
        self.show_goal_message = show_goal_message
        self.node_colors = {}
        self.node_costs = {}
        self.cost_text_ids = {}

    def set_positions(self, positions):
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}

    def reset_colors(self):
        for node in self.node_colors:
            print(f"Resetting Node {node}")
            self.update_node_color(node, COLOR_NOT_VISITED)

        for text_id in self.cost_text_ids.values():
            self.canvas.delete(text_id)
        self.cost_text_ids.clear()

        self.node_costs.clear()

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
