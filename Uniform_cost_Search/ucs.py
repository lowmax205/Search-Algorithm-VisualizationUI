import heapq  # For priority queue implementation

# Define constants for colors
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class USC_Logic:
    def __init__(self, canvas, update_node_color, show_goal_message, update_cost_display):
        self.canvas = canvas
        self.update_node_color = update_node_color
        self.show_goal_message = show_goal_message
        self.update_cost_display = update_cost_display  # Function to update cost display on the UI
        self.node_colors = {}
        self.node_costs = {}  # To store the cost of each node for display

    def set_positions(self, positions):
        # Set node positions and initialize node colors.
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}
        self.node_costs = {node: float('inf') for node in self.positions}  # Initialize costs as infinity

    def reset_colors(self):
        # Reset all node colors to not visited.
        for node in self.node_colors:
            print("Resetting Node", node)
            self.update_node_color(node, COLOR_NOT_VISITED)
            self.update_cost_display(node, "")  # Clear the cost display when resetting

    def ucs(self, start_node, goal_node=None):
        # Perform UCS traversal and visualize the process, stopping if the goal node is found.
        priority_queue = [(0, start_node)]  # Priority queue with (cost, node)
        visited = set()
        costs = {start_node: 0}  # Track the lowest cost to each node
        self.node_costs[start_node] = 0  # Set the start node cost to 0 for visualization

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)  # Pop the least-cost node

            if current_node not in visited:
                print("Visiting:", current_node, "with cost:", current_cost)
                self.update_node_color(current_node, COLOR_VISITING)
                self.update_cost_display(current_node, current_cost)  # Update the displayed cost

            if current_node == goal_node:
                print("Goal:", current_node, "reached with cost:", current_cost)
                self.update_node_color(current_node, COLOR_GOAL)  # Mark goal node as red
                self.update_cost_display(current_node, current_cost)  # Update the displayed cost
                self.show_goal_message(goal_node)
                return

            visited.add(current_node)
            print("Visited:", current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            # Explore neighbors and update the priority queue with new costs
            for neighbor, cost in self.get_neighbors(current_node):
                new_cost = current_cost + cost
                if neighbor not in visited or new_cost < costs.get(neighbor, float('inf')):
                    costs[neighbor] = new_cost
                    self.node_costs[neighbor] = new_cost  # Update the cost for visualization
                    heapq.heappush(priority_queue, (new_cost, neighbor))
                    print("Adding neighbor:", neighbor, "with updated cost:", new_cost)
                    self.update_node_color(neighbor, COLOR_VISITING)
                    self.update_cost_display(neighbor, new_cost)  # Update the displayed cost

    def get_neighbors(self, node):
        # Define neighbors for each node with costs as a tuple (neighbor, cost).
        neighbors = {
            'A': [('B', 1), ('C', 2)],
            'B': [('D', 3), ('E', 4)],
            'C': [('F', 5), ('G', 6)],
            'D': [('H', 7), ('I', 8)],
            'E': [],
            'F': [('J', 9), ('K', 10)],
            'G': [],
            'H': [('L', 11)],
            'I': [('M', 12)],
            'J': [('N', 13)],
            'K': [],
            'L': [],
            'M': [],
            'N': []
        }
        return neighbors.get(node, [])
