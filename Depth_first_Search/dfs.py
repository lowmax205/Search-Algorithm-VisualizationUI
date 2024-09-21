# Define constants for colors
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class DFSLogic:
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
            print("Resetting Node ",node)
            self.update_node_color(node, COLOR_NOT_VISITED)

    def dfs(self, start_node, goal_node=None):
        stack = [start_node]  # Use a stack for DFS
        visited = set()

        while stack:
            current_node = stack.pop()  # Pop from the top of the stack

            if current_node not in visited:
                print("Visiting: ", current_node)
                self.update_node_color(current_node, COLOR_VISITING)

            if current_node == goal_node:
                print("Goal: ", current_node)
                self.update_node_color(current_node, COLOR_GOAL)
                self.show_goal_message(goal_node)
                return

            visited.add(current_node)
            print("Visited: ", current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            # Reverse the order of neighbors before adding to the stack
            for neighbor in reversed(self.get_neighbors(current_node)):
                if neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)  # Push onto the stack
                    print("Visiting neighbor: ", neighbor)
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
