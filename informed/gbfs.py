from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED, reconstruct_path
from source import BaseSearchLogic

class GBFSLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message, update_distance_display=None):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.heuristics = {}
        self.update_distance_display = update_distance_display
        self.distance_text_ids = {}

    def set_heuristics(self, heuristics):
        self.heuristics = heuristics

    def greedy_bfs(self, start_node, goal_node=None):
        open_list = [start_node]
        visited = set()
        parents = {start_node: None}

        while open_list:
            open_list.sort(key=lambda node: self.heuristics.get(node, float('inf')))
            current_node = open_list.pop(0)

            if current_node not in visited:
                print(f"Visiting: {current_node}")
                self.update_node_color(current_node, COLOR_VISITING)

            if current_node == goal_node:
                self.update_node_color(current_node, COLOR_GOAL)
                path, path_costs = reconstruct_path(parents, start_node, goal_node, self.heuristics)
                print(f"Goal: {current_node}")
                self.show_goal_message(goal_node)
                return

            visited.add(current_node)
            print(f"Visited: {current_node}")
            self.update_node_color(current_node, COLOR_VISITED)

            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited and neighbor not in open_list:
                    open_list.append(neighbor)
                    print(f"Adding neighbor: {neighbor}")
                    parents[neighbor] = current_node 

                    if self.update_distance_display:
                        distance = self.heuristics.get(neighbor, 0) 
                        self.update_distance_display(neighbor, distance)

                    self.update_node_color(neighbor, COLOR_VISITING)

        print(f"Goal node '{goal_node}' was not reached.")
