from source import COLOR_START, COLOR_VISITED, COLOR_VISITING, COLOR_GOAL
from source import BaseSearchLogic, reconstruct_path, highlight_path

class DFS_DLSLogic(BaseSearchLogic):
    # Calculate the depth of the goal node from the start node
    def calculate_goal_depth(self, start_node, goal_node):
        queue = [(start_node, 0)]
        visited = set() 

        while queue:
            current_node, depth = queue.pop(0)  

            # If goal node is found, return its depth
            if current_node == goal_node:
                return depth 

            # Explore unvisited nodes
            if current_node not in visited:
                visited.add(current_node)  

                # Add neighbors to the queue
                for neighbor in self.get_neighbors(current_node):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1)) 

        # Return infinity if goal node is not found
        return float('inf') 

    # Depth-Limited Search implementation
    def dls(self, start_node, goal_node=None):
        self.update_node_color(goal_node, COLOR_GOAL)
        # Calculate depth limit or set to infinity if no goal node
        depth_limit = self.calculate_goal_depth(start_node, goal_node) if goal_node else float('inf') 
        stack = [(start_node, 0)] 
        visited = set() 
        current_depth = 0

        parents = {start_node: None}
        next_level_stack = []  

        while stack or next_level_stack:
            # Move to the next depth level if current level is exhausted
            if not stack:
                stack, next_level_stack = next_level_stack, []  
                current_depth += 1
                print(f"Proceeding to depth level {current_depth}")
                # Stop if depth limit is reached
                if current_depth > depth_limit:
                    print("Depth limit reached. Stopping further exploration.")
                    return
            current_node, depth = stack.pop()  

            # Process unvisited nodes
            if current_node not in visited:
                print("Visiting:", current_node)
                self.update_node_color(current_node, COLOR_VISITING) 

                # Check if goal node is reached
                if current_node == goal_node:
                    path, _x = reconstruct_path(parents, start_node, goal_node, self.node_costs)
                    highlight_path(self, path, start_node, goal_node)
                    print(f"Goal node: {current_node}")
                    self.update_node_color(current_node, COLOR_GOAL) 
                    self.show_goal_message(goal_node)
                    return path

                # Mark node as visited
                visited.add(current_node)
                print("Visited:", current_node)
                self.update_node_color(current_node, COLOR_VISITED) 

                # Explore neighbors
                for neighbor in reversed(self.get_neighbors(current_node)):
                    if neighbor not in visited and all(neighbor != n for n, d in stack + next_level_stack):
                        # Add neighbor to appropriate stack based on depth
                        if depth == current_depth:
                            next_level_stack.append((neighbor, depth + 1))  
                        else:
                            stack.append((neighbor, depth + 1))  

                        parents[neighbor] = current_node 
                        print("Adding neighbor:", neighbor, "at depth:", depth + 1)
                        self.update_node_color(neighbor, COLOR_VISITING) 
                        
        print("No path found")
        return None  # If no path is found
