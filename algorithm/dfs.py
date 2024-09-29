from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class DFSLogic(BaseSearchLogic):
    def dfs(self, start_node, goal_node=None):
        stack = [start_node]
        visited = set()

        while stack:
            current_node = stack.pop()  # Pop the top node from the stack

            if current_node not in visited:
                print(f"Visiting: {current_node}")
                self.update_node_color(current_node, COLOR_VISITING)  # Mark node as being visited

            if current_node == goal_node:
                print(f"Goal: {current_node}")
                self.update_node_color(current_node, COLOR_GOAL)  # Goal node found
                self.show_goal_message(goal_node)  # Notify goal achievement
                return

            visited.add(current_node)  # Mark current node as visited
            print(f"Visited: {current_node}")
            self.update_node_color(current_node, COLOR_VISITED)  # Mark node as fully explored

            for neighbor in reversed(self.get_neighbors(current_node)):  # Reverse for DFS order
                if neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)  # Add unvisited neighbors to the stack
                    print(f"Visiting neighbor: {neighbor}")
                    self.update_node_color(neighbor, COLOR_VISITING)  # Mark neighbor as being visited
