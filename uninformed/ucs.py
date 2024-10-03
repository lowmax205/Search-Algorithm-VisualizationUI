import heapq 
from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class UCSLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message, update_cost_display):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.update_cost_display = update_cost_display
        self.node_costs = {}
        
    def ucs(self, start_node, goal_node=None):
        priority_queue = [(0, start_node)] 
        visited = set()
        costs = {start_node: 0}
        self.node_costs[start_node] = 0

        while priority_queue:
            current_cost, current_node = heapq.heappop(priority_queue)
            
            if current_node not in visited:
                print("Visiting: ", current_node, "with cumulative cost: ", current_cost)
                self.update_node_color(current_node, COLOR_VISITING) 
                self.update_cost_display(current_node, current_cost)

            if current_node == goal_node:
                total_cost = costs[goal_node] 
                print("Goal: ", current_node, "reached with total cost of: ", total_cost)
                self.update_node_color(current_node, COLOR_GOAL)
                self.update_cost_display(current_node, total_cost)
                self.show_goal_message(f"Goal node '{goal_node}' reached with a total cost of {total_cost}")
                return

            visited.add(current_node)
            print("Visited: ", current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            for neighbor, cost in self.ucs_get_neighbors(current_node):
                new_cost = current_cost + cost
                if neighbor not in visited or new_cost < costs.get(neighbor, float('inf')):
                    costs[neighbor] = new_cost
                    self.node_costs[neighbor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor)) 
                    self.update_node_color(neighbor, COLOR_VISITING)
                    self.update_cost_display(neighbor, new_cost)
