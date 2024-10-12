from source import COLOR_START, COLOR_VISITED, COLOR_VISITING, COLOR_GOAL
from source import BaseSearchLogic, reconstruct_path, highlight_path
import heapq

class UCSLogic(BaseSearchLogic):
    # Implements Uniform Cost Search (UCS) algorithm
    def __init__(self, canvas, update_node_color, show_goal_message, update_cost_display):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.update_cost_display = update_cost_display
        self.node_costs = {}
        self.parents = {}
        
    def ucs(self, start_node, goal_node=None):
        self.update_node_color(goal_node, COLOR_GOAL)
        # Initialize UCS data structures
        total_travel_cost = 0
        priority_queue = [(0, start_node)]
        visited = set()
        costs = {start_node: 0}
        self.node_costs[start_node] = 0
        self.parents[start_node] = None

        # Main UCS loop
        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)
            
            total_travel_cost += current_cost
            
            # Process unvisited nodes
            if current_node not in visited:
                print("Visiting:", current_node, "with cost:", current_cost)
                self.update_node_color(current_node, COLOR_VISITING)
                self.update_cost_display(current_node, current_cost)

            # Check if goal node is reached
            if current_node == goal_node:
                path, path_costs = reconstruct_path(self.parents, start_node, goal_node, self.node_costs)
                highlight_path(self, path, start_node, goal_node)
                self.update_node_color(current_node, COLOR_GOAL)
                self.update_cost_display(current_node, current_cost)
                self.show_goal_message(f"Goal node '{goal_node}' reached. Total path cost: {sum(path_costs)}")
                return path

            # Mark node as visited
            visited.add(current_node)
            print("Visited:", current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            # Explore neighbors
            for neighbor, cost in self.ucs_get_neighbors(current_node):
                new_cost = current_cost + cost
                if neighbor not in visited or new_cost < costs.get(neighbor, float('inf')):
                    costs[neighbor] = new_cost
                    self.node_costs[neighbor] = new_cost
                    self.parents[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_cost, neighbor))
                    self.update_node_color(neighbor, COLOR_VISITING)
                    self.update_cost_display(neighbor, new_cost)

        print(f"Goal node '{goal_node}' was not reached. Total travel cost: {total_travel_cost}")
