# Define constants for colors
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class IDS_Logic:
    def __init__(self, update_node_color, show_goal_message):
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
            print("Resetting Node", node)
            self.update_node_color(node, COLOR_NOT_VISITED)

    def ids(self, start_node, goal_node=None):
        # Perform IDS traversal with progressively increasing depth.
        depth = 0
        while True:
            print(f"Exploring with depth limit: {depth}")
            self.reset_colors()  # Reset the colors at the start of each new depth level
            found = self.dls(start_node, goal_node, depth)
            if found:
                return
            depth += 1

    def dls(self, start_node, goal_node, depth_limit):
        # Perform Depth-Limited Search (DLS) with a level-by-level approach.
        # Queue maintains nodes at each depth level, starting with the initial node.
        current_level = [(start_node, 0)]  # Current level with the starting node and depth 0.
        next_level = []  # Prepare the next level list.
        visited = set()  # Track visited nodes.

        while current_level or next_level:
            # If current level is empty, move to the next level.
            if not current_level:
                current_level, next_level = next_level, []  # Swap levels and go deeper.
                print(f"Proceeding to depth level: {current_level[0][1]}")

            # Get node and its depth from the current level.
            node, depth = current_level.pop(0)
            
            # Skip nodes exceeding the current depth limit.
            if depth > depth_limit:
                continue
            
            if node not in visited:
                print(f"Visiting: {node} at depth {depth}")
                self.update_node_color(node, COLOR_VISITING)

                # Check if the node is the goal.
                if node == goal_node:
                    print(f"Goal: {node} reached.")
                    self.update_node_color(node, COLOR_GOAL)
                    self.show_goal_message(goal_node)
                    return True

                # Mark as visited and update color.
                visited.add(node)
                self.update_node_color(node, COLOR_VISITED)

                # Add neighbors to the next level only if within allowed depth.
                if depth < depth_limit:
                    for neighbor in self.get_neighbors(node):
                        if neighbor not in visited:
                            next_level.append((neighbor, depth + 1))
                            print(f"Adding Neighbor: {neighbor} at depth {depth + 1}")

        return False

    def get_neighbors(self, node):
        # Define neighbors for each node.
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
