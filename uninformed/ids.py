from source import COLOR_VISITED, COLOR_VISITING, COLOR_GOAL
from source import BaseSearchLogic

class IDSLogic(BaseSearchLogic):
    # Implements Iterative Deepening Search (IDS)
    def ids(self, start_node, goal_node=None):
        max_depth = 5 # Default depth limit
        for depth in range(max_depth):
            print(f"Exploring with depth limit: {depth}")
            found = self.dls(start_node, goal_node, depth) 
            if found:
                return found
            self.reset_colors()
            if not found and depth == max_depth - 1:
                return None  # If no path is found after exploring all depths

    # Implements Depth-Limited Search (DLS)
    def dls(self, start_node, goal_node, depth_limit):
        self.update_node_color(goal_node, COLOR_GOAL)
        current_level = [(start_node, 0)] 
        next_level = [] 
        visited = set() 
        parents = {start_node: None} 

        while current_level or next_level:
            # Move to next depth level if current level is exhausted
            if not current_level:
                current_level, next_level = next_level, []
                if current_level:
                    print(f"Proceeding to depth level: {current_level[0][1]}")

            current_node, depth = current_level.pop(0) 
            
            # Process unvisited nodes
            if current_node not in visited:
                print(f"Visiting: {current_node} at depth {depth}")
                self.update_node_color(current_node, COLOR_VISITING)  

                # Check if goal node is reached
                if current_node == goal_node:
                    path, _x = self.reconstruct_path(parents, start_node, goal_node, self.node_costs)
                    self.highlight_path(path, start_node, goal_node)
                    print(f"Goal node: {current_node}")
                    self.update_node_color(current_node, COLOR_GOAL) 
                    self.show_goal_message(goal_node)
                    return path

                # Mark node as visited
                visited.add(current_node) 
                self.update_node_color(current_node, COLOR_VISITED)

                # Explore neighbors within depth limit
                if depth < depth_limit:  
                    for neighbor in self.get_neighbors(current_node):
                        if neighbor not in visited:
                            next_level.append((neighbor, depth + 1)) 
                            parents[neighbor] = current_node  
                            print(f"Adding Neighbor: {neighbor} at depth {depth + 1}")
        
        print("No path found")
        return None
