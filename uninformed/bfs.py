from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED, reconstruct_path
from source import BaseSearchLogic

class BFSLogic(BaseSearchLogic):
    # Implementation of Breadth-First Search algorithm
    def bfs(self, start_node, goal_node=None):
        # Initialize the queue with the start node
        queue = [start_node]  
        # Keep track of visited nodes
        visited = set()
        # Store parent nodes for path reconstruction
        parents = {start_node: None}

        while queue:
            # Get the next node from the front of the queue
            current_node = queue.pop(0) 

            # Check if the current node has not been visited
            if current_node not in visited:
                print(f"Visiting: {current_node}")
                self.update_node_color(current_node, COLOR_VISITING) 

            # Check if the current node is the goal
            if current_node == goal_node:
                # Reconstruct and display the path to the goal
                reconstruct_path(parents, start_node, goal_node, self.node_costs)
                print(f"Goal node: {current_node}")
                self.update_node_color(current_node, COLOR_GOAL) 
                self.show_goal_message(goal_node) 
                return

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
        return None  # If no path is found
