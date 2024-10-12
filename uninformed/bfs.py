from source import COLOR_VISITED, COLOR_VISITING, COLOR_GOAL
from source import BaseSearchLogic, reconstruct_path, highlight_path

class BFSLogic(BaseSearchLogic):
    # Implementation of Breadth-First Search algorithm
    def bfs(self, start_node, goal_node=None):
        self.update_node_color(goal_node, COLOR_GOAL)
        # Initialize the queue with the start node
        queue = [start_node]  
        # Keep track of visited nodes
        visited = set()
        # Store parent nodes for path reconstruction
        parents = {start_node: None}

        while queue:
            # Get the next node from the front of the queue
            current_node = queue.pop(0) 
            # Check if the current node is the goal
            if current_node == goal_node: 
                # Reconstruct and display the path to the goal
                path = reconstruct_path(parents, start_node, goal_node, self.node_costs)[0]
                highlight_path(self, path, start_node, goal_node)
                print(f"Goal node: {current_node}")
                self.show_goal_message(goal_node)
                return path

            # Mark the current node as visited
            visited.add(current_node) 
            print(f"Visited: {current_node}")
            self.update_node_color(current_node, COLOR_VISITED)  

            # Explore neighbors of the current node
            for neighbor in self.get_neighbors(current_node):
                # Add unvisited neighbors to the queue
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)  
                    parents[neighbor] = current_node 
                    print(f"Visiting neighbor: {neighbor}")
                    self.update_node_color(neighbor, COLOR_VISITING) 

        print("No path found")
        return None  # If no path is found
