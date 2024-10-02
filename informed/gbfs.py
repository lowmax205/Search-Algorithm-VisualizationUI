from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class GBFSLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message):
        super().__init__(canvas, update_node_color, show_goal_message)
        self.heuristics = {}  # Dictionary to store heuristics

    def set_heuristics(self, heuristics):
        self.heuristics = heuristics  # Set heuristics

    def greedy_bfs(self, start_node, goal_node=None):
        open_list = [start_node]  # Initialize open list with the start node
        visited = set()  # Track visited nodes

        while open_list:
            open_list.sort(key=lambda node: self.heuristics.get(node, float('inf')))  # Sort nodes based on heuristic
            current_node = open_list.pop(0)  # Pop node with the lowest heuristic

            if current_node not in visited:
                print(f"Visiting: {current_node}")
                self.update_node_color(current_node, COLOR_VISITING)  # Mark node as visiting

            if current_node == goal_node:  # If the goal is found, stop
                print(f"Goal: {current_node}")
                self.update_node_color(current_node, COLOR_GOAL)
                self.show_goal_message(goal_node)
                return

            visited.add(current_node)  # Mark node as visited
            print(f"Visited: {current_node}")
            self.update_node_color(current_node, COLOR_VISITED)

            for neighbor in self.get_neighbors(current_node):  # Explore neighbors
                if neighbor not in visited and neighbor not in open_list:
                    open_list.append(neighbor)  # Add unvisited neighbors to the open list
                    print(f"Visiting neighbor: {neighbor}")
                    self.update_node_color(neighbor, COLOR_VISITING)
