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

    def set_positions(self, positions):
        # Set node positions and initialize node colors
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}

    def reset_colors(self):
        # Reset all node colors to not visited
        for node in self.node_colors:
            print(f"Resetting Node {node}")
            self.update_node_color(node, COLOR_NOT_VISITED)

    def get_neighbors(self, node):
        # Define neighbors for each node
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
