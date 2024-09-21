# Define constants for colors
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class BFSLogic:
    def __init__(self, canvas, update_node_color, show_goal_message):
        self.canvas = canvas
        self.update_node_color = update_node_color
        self.show_goal_message = show_goal_message
        self.node_colors = {}

    def set_positions(self, positions):
        # Set node positions and initialize node colors.
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}

    def reset_colors(self):
        # Reset all node colors to not visited.
        for node in self.node_colors:
            self.update_node_color(node, COLOR_NOT_VISITED)

    def bfs(self, start_node, goal_node=None):
        # Perform BFS traversal and visualize the process, stopping if the goal node is found.
        queue = [start_node]
        visited = set()

        while queue:
            current_node = queue.pop(0)

            if current_node not in visited:
                self.update_node_color(current_node, COLOR_VISITING)

            if current_node == goal_node:
                self.update_node_color(current_node, COLOR_GOAL)  # Mark goal node as red
                self.show_goal_message(goal_node)
                return

            visited.add(current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)
                    self.update_node_color(neighbor, COLOR_VISITING)

    def get_neighbors(self, node):
        # Define neighbors for each node as a simple adjacency list.
        neighbors = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F', 'G'],
            'D': [],
            'E': [],
            'F': [],
            'G': []
        }
        return neighbors.get(node, [])
