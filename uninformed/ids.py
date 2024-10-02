from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class IDSLogic(BaseSearchLogic):
    def ids(self, start_node, goal_node=None):
        depth = 0
        while True:
            print(f"Exploring with depth limit: {depth}")
            found = self.dls(start_node, goal_node, depth)  # Perform depth-limited search
            if found:
                return  # Stop if goal is found
            depth += 1  # Increase depth for the next iteration
            self.reset_colors()  # Reset colors

    def dls(self, start_node, goal_node, depth_limit):
        current_level = [(start_node, 0)]  # Initialize current level with start node and depth
        next_level = []  # Track nodes for the next level
        visited = set()  # Track visited nodes

        while current_level or next_level:
            if not current_level:
                current_level, next_level = next_level, []  # Move to the next depth level
                if current_level:
                    print(f"Proceeding to depth level: {current_level[0][1]}")

            node, depth = current_level.pop(0)  # Pop a node for exploration

            if depth > depth_limit:  # Skip if depth exceeds the limit
                continue
            
            if node not in visited:
                print(f"Visiting: {node} at depth {depth}")
                self.update_node_color(node, COLOR_VISITING)  # Mark node as visiting

                if node == goal_node:  # If goal is reached, stop
                    print(f"Goal: {node} reached.")
                    self.update_node_color(node, COLOR_GOAL)
                    self.show_goal_message(goal_node)
                    return True

                visited.add(node)  # Mark node as visited
                self.update_node_color(node, COLOR_VISITED)

                if depth < depth_limit:  # Explore neighbors if depth allows
                    for neighbor in self.get_neighbors(node):
                        if neighbor not in visited:
                            next_level.append((neighbor, depth + 1))  # Add neighbors to the next level
                            print(f"Adding Neighbor: {neighbor} at depth {depth + 1}")
        return False