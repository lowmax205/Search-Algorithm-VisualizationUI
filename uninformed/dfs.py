from source import COLOR_VISITED, COLOR_VISITING, COLOR_GOAL
from source import BaseSearchLogic, reconstruct_path, highlight_path

class DFSLogic(BaseSearchLogic):
    # Implementation of Depth-First Search algorithm
    def dfs(self, start_node, goal_node=None):
        self.update_node_color(goal_node, COLOR_GOAL)
        # Initialize the stack with the start node
        stack = [start_node]
        # Keep track of visited nodes
        visited = set()
        # Store parent nodes for path reconstruction
        parents = {start_node: None}

        while stack:
            # Get the next node from the top of the stack
            current_node = stack.pop()
            # Check if the current node is the goal
            if current_node == goal_node:
                # Reconstruct and display the path to the goal
                path, _x = reconstruct_path(parents, start_node, goal_node, self.node_costs)
                highlight_path(self, path, start_node, goal_node)
                print(f"Goal node: {current_node}")
                self.show_goal_message(goal_node) 
                return path

            # Mark the current node as visited
            visited.add(current_node)  
            print(f"Visited: {current_node}")
            self.update_node_color(current_node, COLOR_VISITED) 

            # Explore neighbors of the current node
            for neighbor in reversed(self.get_neighbors(current_node)): 
                # Add unvisited neighbors to the stack
                if neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)
                    parents[neighbor] = current_node
                    print(f"Visiting neighbor: {neighbor}")
                    self.update_node_color(neighbor, COLOR_VISITING) 
                    
        print("No path found")
        return None  # If no path is found
