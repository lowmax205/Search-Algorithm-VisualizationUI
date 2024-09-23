# Define constants for colors
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class DFS_DLSLogic:
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

    def calculate_goal_depth(self, start_node, goal_node):
        # Calculate the depth of the goal node using BFS to determine depth levels.
        queue = [(start_node, 0)]  # Queue for BFS with depth tracking
        visited = set()  # Track visited nodes

        while queue:
            current_node, depth = queue.pop(0)  # Dequeue the node and its current depth

            if current_node == goal_node:
                return depth  # Return the depth when the goal node is found

            if current_node not in visited:
                visited.add(current_node)

                # Enqueue all unvisited neighbors with incremented depth
                for neighbor in self.get_neighbors(current_node):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))

        return float('inf')  # Return infinity if the goal is not reachable


    def dls(self, start_node, goal_node=None):
        # Perform Depth-Limited Search (DLS) with strict level-by-level exploration.
        # Determine the depth limit based on goal location, or set to infinity if no goal is specified
        depth_limit = self.calculate_goal_depth(start_node, goal_node) if goal_node else float('inf')

        # Stack stores tuples of (node, depth)
        stack = [(start_node, 0)]
        visited = set()
        current_depth = 0

        # Use a temporary stack to collect nodes for the next level after exploring current level
        next_level_stack = []

        while stack or next_level_stack:
            # Check if all nodes at the current depth level have been processed
            if not stack:
                # Move to the next level by swapping stacks
                stack, next_level_stack = next_level_stack, []
                current_depth += 1
                print(f"Proceeding to depth level {current_depth}")

                # Stop if current depth exceeds the depth limit
                if current_depth > depth_limit:
                    print("Depth limit reached. Stopping further exploration.")
                    return

            # Pop node and its depth from the stack
            current_node, depth = stack.pop()

            if current_node not in visited:
                print("Visiting:", current_node)
                self.update_node_color(current_node, COLOR_VISITING)

                # Check if the current node is the goal
                if current_node == goal_node:
                    print("Goal:", current_node)
                    self.update_node_color(current_node, COLOR_GOAL)
                    self.show_goal_message(goal_node)
                    return

                visited.add(current_node)
                print("Visited:", current_node)
                self.update_node_color(current_node, COLOR_VISITED)

                # Explore neighbors only if within the allowed depth
                for neighbor in reversed(self.get_neighbors(current_node)):
                    if neighbor not in visited and all(neighbor != n for n, d in stack + next_level_stack):
                        if depth == current_depth:
                            # Add neighbors to the next level stack if still on the current level
                            next_level_stack.append((neighbor, depth + 1))
                        else:
                            # Regular addition to the stack if we're just visiting nodes
                            stack.append((neighbor, depth + 1))

                        print("Adding neighbor:", neighbor, "at depth:", depth + 1)
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
