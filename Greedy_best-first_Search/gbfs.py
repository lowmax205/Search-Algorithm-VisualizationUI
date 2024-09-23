# Define constants for colors
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class GBFSLogic:
    def __init__(self, canvas, update_node_color, show_goal_message):
        self.canvas = canvas
        self.update_node_color = update_node_color
        self.show_goal_message = show_goal_message
        self.node_colors = {}
        self.heuristics = {}  # Holds heuristic values for each node

    def set_positions(self, positions):
        # Set initial positions and colors for nodes.
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in positions}

    def set_heuristics(self, heuristics):
        # Set heuristic values for nodes.
        self.heuristics = heuristics

    def reset_colors(self):
        # Reset all node colors to not visited.
        for node in self.node_colors:
            self.update_node_color(node, COLOR_NOT_VISITED)

    def greedy_bfs(self, start_node, goal_node=None):
        # Perform Greedy Best-First Search and visualize the process.
        open_list = [start_node]
        visited = set()

        while open_list:
            # Sort open_list based on heuristic values
            open_list.sort(key=lambda node: self.heuristics.get(node, float('inf')))
            current_node = open_list.pop(0)

            # Mark as visiting
            if current_node not in visited:
                print("Visiting: ", current_node)
                self.update_node_color(current_node, COLOR_VISITING)

            # Check if goal is reached
            if current_node == goal_node:
                print("Goal: ", current_node)
                self.update_node_color(current_node, COLOR_GOAL)
                self.show_goal_message(goal_node)
                return

            # Mark node as visited
            visited.add(current_node)
            print("Visited: ", current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            # Add neighbors based on adjacency
            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited and neighbor not in open_list:
                    open_list.append(neighbor)
                    print("Visiting neighbor: ", neighbor)
                    self.update_node_color(neighbor, COLOR_VISITING)

    def get_neighbors(self, node):
        # Define neighbors for each node as a simple adjacency list.
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
