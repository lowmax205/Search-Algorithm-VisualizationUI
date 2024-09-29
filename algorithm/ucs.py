import heapq 
from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class UCSLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message, update_cost_display):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.update_cost_display = update_cost_display  # Function to update cost display
        self.node_costs = {}  # Dictionary to store costs for each node
        
    def ucs(self, start_node, goal_node=None):
        priority_queue = [(0, start_node)]  # Initialize priority queue with start node and cost 0
        visited = set()  # Track visited nodes
        costs = {start_node: 0}  # Track costs for each node
        self.node_costs[start_node] = 0  # Set initial cost for the start node

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)  # Pop node with the lowest cost

            if current_node not in visited:
                print("Visiting:", current_node, "with cost:", current_cost)
                self.update_node_color(current_node, COLOR_VISITING)  # Mark node as visiting
                self.update_cost_display(current_node, current_cost)  # Display the current cost

            if current_node == goal_node:  # If the goal is reached, stop
                print("Goal: ", current_node, "reached with cost:", current_cost)
                self.update_node_color(current_node, COLOR_GOAL)
                self.update_cost_display(current_node, current_cost)  # Display the final cost
                self.show_goal_message(goal_node)
                return

            visited.add(current_node)  # Mark node as visited
            print("Visited: ", current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            for neighbor, cost in self.ucs_get_neighbors(current_node):  # Explore neighbors with costs
                new_cost = current_cost + cost  # Calculate new cost for the neighbor
                if neighbor not in visited or new_cost < costs.get(neighbor, float('inf')):
                    costs[neighbor] = new_cost  # Update cost if it's lower
                    self.node_costs[neighbor] = new_cost  # Store the cost
                    heapq.heappush(priority_queue, (new_cost, neighbor))  # Add neighbor to the priority queue
                    self.update_node_color(neighbor, COLOR_VISITING)
                    self.update_cost_display(neighbor, new_cost)  # Display the new cost
