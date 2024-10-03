import heapq
from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class UCSLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message, update_cost_display):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.update_cost_display = update_cost_display
        self.node_costs = {}
        self.parents = {}
        
    def ucs(self, start_node, goal_node=None):
        total_travel_cost = 0
        priority_queue = [(0, start_node)]
        visited = set()
        costs = {start_node: 0}
        self.node_costs[start_node] = 0
        self.parents[start_node] = None

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)
            
            # Accumulate the total cost for all visited nodes (including non-optimal ones)
            total_travel_cost += current_cost
            
            if current_node not in visited:
                print("Visiting:", current_node, "with cost:", current_cost)
                self.update_node_color(current_node, COLOR_VISITING)
                self.update_cost_display(current_node, current_cost)

            if current_node == goal_node:
                # When the goal is reached, print the path and total cost
                print("Goal:", current_node, "reached with travel cost:", total_travel_cost)
                path, path_costs = self.reconstruct_path(start_node, goal_node, costs)
                print("Path:", " -> ".join(path))
                print("Path costs:", path_costs)
                print(f"Total path cost: {sum(path_costs)}")
                
                # Update display for the goal node
                self.update_node_color(current_node, COLOR_GOAL)
                self.update_cost_display(current_node, current_cost)
                self.show_goal_message(f"Goal node '{goal_node}' reached. Total path cost: {sum(path_costs)}")
                return

            visited.add(current_node)
            print("Visited:", current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            for neighbor, cost in self.ucs_get_neighbors(current_node):
                new_cost = current_cost + cost
                if neighbor not in visited or new_cost < costs.get(neighbor, float('inf')):
                    costs[neighbor] = new_cost
                    self.node_costs[neighbor] = new_cost
                    self.parents[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_cost, neighbor))
                    self.update_node_color(neighbor, COLOR_VISITING)
                    self.update_cost_display(neighbor, new_cost)

        # If the loop exits without finding the goal
        print(f"Goal node '{goal_node}' was not reached. Total travel cost: {total_travel_cost}")
        
    #Reconstruct the path from start_node to goal_node and return it with the path costs.
    def reconstruct_path(self, start_node, goal_node, costs):
        
        path = []
        path_costs = []
        current_node = goal_node
        
        while current_node is not None:
            path.append(current_node)
            path_costs.append(costs[current_node])
            current_node = self.parents[current_node]

        path.reverse()
        path_costs.reverse()
        return path, path_costs
