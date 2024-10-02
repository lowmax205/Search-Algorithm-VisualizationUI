from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class DFS_DLSLogic(BaseSearchLogic):
    def calculate_goal_depth(self, start_node, goal_node):
        queue = [(start_node, 0)]
        visited = set() 

        while queue:
            current_node, depth = queue.pop(0)  # Dequeue the front node

            if current_node == goal_node:
                return depth  # Return the depth at which the goal is found

            if current_node not in visited:
                visited.add(current_node)  # Mark node as visited

                for neighbor in self.get_neighbors(current_node):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))  # Add neighbors with updated depth

        return float('inf')  # Return infinity if goal not found

    def dls(self, start_node, goal_node=None):
        depth_limit = self.calculate_goal_depth(start_node, goal_node) if goal_node else float('inf')  # Set depth limit
        stack = [(start_node, 0)]  # Initialize stack with start node and depth 0
        visited = set()  # Set to track visited nodes
        current_depth = 0

        next_level_stack = []  # Stack for next level nodes

        while stack or next_level_stack:
            if not stack:
                stack, next_level_stack = next_level_stack, []  # Move to the next depth level
                current_depth += 1
                print(f"Proceeding to depth level {current_depth}")
                if current_depth > depth_limit:
                    print("Depth limit reached. Stopping further exploration.")
                    return
            current_node, depth = stack.pop()  # Pop top node from the stack

            if current_node not in visited:
                print("Visiting:", current_node)
                self.update_node_color(current_node, COLOR_VISITING)  # Mark node as being visited

                if current_node == goal_node:
                    print("Goal:", current_node)
                    self.update_node_color(current_node, COLOR_GOAL)  # Goal node found
                    self.show_goal_message(goal_node)  # Notify goal achievement
                    return

                visited.add(current_node)  # Mark node as visited
                print("Visited:", current_node)
                self.update_node_color(current_node, COLOR_VISITED)  # Mark node as fully explored

                for neighbor in reversed(self.get_neighbors(current_node)):
                    if neighbor not in visited and all(neighbor != n for n, d in stack + next_level_stack):
                        if depth == current_depth:
                            next_level_stack.append((neighbor, depth + 1))  # Add to next level
                        else:
                            stack.append((neighbor, depth + 1))  # Add to current level stack

                        print("Adding neighbor:", neighbor, "at depth:", depth + 1)
                        self.update_node_color(neighbor, COLOR_VISITING)  # Mark neighbor as being visited
