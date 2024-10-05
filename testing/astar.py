from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class AStarLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.heuristics = {}
        self.g_costs = {}

    def set_heuristics(self, heuristics):
        self.heuristics = heuristics

    def a_star(self, start_node, goal_node=None):
        open_list = [start_node]
        visited = set()
        self.g_costs = {start_node: 0}

        while open_list:
            open_list.sort(key=lambda node: self.g_costs.get(node, float('inf')) + self.heuristics.get(node, float('inf')))
            current_node = open_list.pop(0)

            self.update_node_color(current_node, COLOR_VISITING)

            if current_node == goal_node:
                self.update_node_color(current_node, COLOR_GOAL)
                self.show_goal_message(goal_node)
                return

            visited.add(current_node)
            self.update_node_color(current_node, COLOR_VISITED)

            for neighbor in self.get_neighbors(current_node):
                tentative_g_cost = self.g_costs[current_node] + self.get_edge_weight(current_node, neighbor)

                if neighbor not in visited and (neighbor not in open_list or tentative_g_cost < self.g_costs.get(neighbor, float('inf'))):
                    self.g_costs[neighbor] = tentative_g_cost
                    open_list.append(neighbor)
                    self.update_node_color(neighbor, COLOR_VISITING)

        print("Goal not reachable from the starting node.")

