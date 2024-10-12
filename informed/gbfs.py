from source import COLOR_VISITED, COLOR_VISITING, COLOR_GOAL
from source import BaseSearchLogic, reconstruct_path, highlight_path

class GBFSLogic(BaseSearchLogic):
    # Implements Greedy Best-First Search (GBFS) algorithm
    def __init__(self, canvas, update_node_color, show_goal_message, update_distance_display=None):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.heuristics = {}
        self.update_distance_display = update_distance_display
        self.distance_text_ids = {}

    def set_heuristics(self, heuristics):
        self.heuristics = heuristics

    def greedy_bfs(self, start_node, goal_node=None):
        self.update_node_color(goal_node, COLOR_GOAL)
        # Initialize GBFS data structures
        open_list = [start_node]
        visited = set()
        parents = {start_node: None}

        # Main GBFS loop
        while open_list:
            # Sort open list based on heuristic values
            open_list.sort(key=lambda node: self.heuristics.get(node, float('inf')))
            current_node = open_list.pop(0)

            # Check if goal node is reached
            if current_node == goal_node:
                path, path_costs = reconstruct_path(parents, start_node, goal_node, self.heuristics)
                highlight_path(self, path, start_node, goal_node)
                print(f"Goal: {current_node}")
                self.show_goal_message(goal_node)
                return path

            # Mark node as visited
            visited.add(current_node)
            print(f"Visited: {current_node}")
            self.update_node_color(current_node, COLOR_VISITED)

            # Explore neighbors
            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited and neighbor not in open_list:
                    open_list.append(neighbor)
                    print(f"Adding neighbor: {neighbor}")
                    parents[neighbor] = current_node 

                    # Update distance display if available
                    if self.update_distance_display:
                        distance = self.heuristics.get(neighbor, 0) 
                        self.update_distance_display(neighbor, distance)

                    self.update_node_color(neighbor, COLOR_VISITING)

        print(f"Goal node '{goal_node}' was not reached.")
        return None
