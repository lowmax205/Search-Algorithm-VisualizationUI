import time
# Define constants for colors to be used for marking the status of nodes
COLOR_START = 'green'
COLOR_VISITED = 'orange'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'
COLOR_PATH = 'blue'
time_seconds = 0.5
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

class BaseSearchLogic:
    # Initialize with canvas, functions to update node color and show goal message
    def __init__(self, canvas, update_node_color, show_goal_message, node_lines):
        self.canvas = canvas  
        self.update_node_color = update_node_color 
        self.show_goal_message = show_goal_message 
        self.node_colors = {}  
        self.node_costs = {}
        self.cost_text_ids = {}
        self.node_lines = node_lines

    # Set positions for nodes and initialize their colors to 'not visited'
    def set_positions(self, positions):
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}
        
    # Reset all node colors to 'not visited'
    def reset_colors(self, change = False):
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.node_colors}
        for _, line in self.node_lines.items():
            self.canvas.itemconfig(line, fill='black')
        for node in self.node_colors:
            self.update_node_color(node, COLOR_NOT_VISITED, animate=False)
            
        if change:
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
    
    def reconstruct_path(self, parents, start_node, goal_node, costs=None):
        path = []
        path_costs = []
        current = goal_node

        # Ensure current is a valid node in parents
        while current is not None:
            path.append(current)
            if costs is not None:
                path_costs.append(costs.get(current, 0))
            # Safeguard against KeyError
            if current in parents:
                current = parents[current]
            else:
                break  # Exit if there's no parent entry for current

        path.reverse()

        print(f"Starting Node: {start_node}")
        print("Path found:", " -> ".join(path))
        if costs:
            print("Path costs:", path_costs)
            print(f"Total path cost: {sum(path_costs)}")

        return path, path_costs

    def highlight_path(self, path, start_node, goal_node):
        # Reset all lines to default color
        for _, line in self.node_lines.items():
            self.canvas.itemconfig(line, fill='black')
            
        # Animate both node and line color changes
        for i in range(len(path)):
            node = path[i]
            color = COLOR_START if node == start_node else COLOR_GOAL if node == goal_node else COLOR_PATH
            self.update_node_color(node, color)
            
            if i > 0:
                prev_node = path[i - 1]
                # Check both possible orientations of the edge
                if (prev_node, node) in self.node_lines:
                    self.canvas.itemconfig(self.node_lines[(prev_node, node)], fill=COLOR_PATH)
                elif (node, prev_node) in self.node_lines:
                    self.canvas.itemconfig(self.node_lines[(node, prev_node)], fill=COLOR_PATH)
            
            self.canvas.update()  # Update the canvas to show the color change
            time.sleep(time_seconds)
            
            