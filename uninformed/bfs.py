from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class BFSLogic(BaseSearchLogic):
    def bfs(self, start_node, goal_node=None):
        queue = [start_node]  
        visited = set()
        parents = {start_node: None}  # Dictionary to track the path

        while queue:
            current_node = queue.pop(0) 

            if current_node not in visited:
                print(f"Visiting: {current_node}")
                self.update_node_color(current_node, COLOR_VISITING) 

            if current_node == goal_node:
                # When the goal is reached, print the path
                path = self.reconstruct_path(parents, goal_node)
                print("Path found:", " -> ".join(path))
                
                print(f"Goal: {current_node}")
                self.update_node_color(current_node, COLOR_GOAL) 
                self.show_goal_message(goal_node) 
                return

            visited.add(current_node) 
            print(f"Visited: {current_node}")
            self.update_node_color(current_node, COLOR_VISITED)  

            for neighbor in self.get_neighbors(current_node):
                if neighbor not in visited and neighbor not in queue:
                    # Add unvisited neighbors to the queue
                    queue.append(neighbor)  
                    parents[neighbor] = current_node 
                    print(f"Visiting neighbor: {neighbor}")
                    self.update_node_color(neighbor, COLOR_VISITING) 

    def reconstruct_path(self, parents, goal_node):
        path = []
        current_node = goal_node

        while current_node is not None:
            path.append(current_node)
            current_node = parents[current_node]  # Move to the parent
        
        path.reverse()  # Reverse the path to get it from start to goal
        return path
