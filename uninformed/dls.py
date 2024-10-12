from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class DFS_DLSLogic(BaseSearchLogic):
    def calculate_goal_depth(self, start_node, goal_node):
        queue = [(start_node, 0)]
        visited = set() 

        while queue:
            current_node, depth = queue.pop(0)  

            if current_node == goal_node:
                return depth 

            if current_node not in visited:
                visited.add(current_node)  

                for neighbor in self.get_neighbors(current_node):
                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1)) 

        return float('inf') 

    def dls(self, start_node, goal_node=None):
        depth_limit = self.calculate_goal_depth(start_node, goal_node) if goal_node else float('inf') 
        stack = [(start_node, 0)] 
        visited = set() 
        current_depth = 0

        parents = {start_node: None}
        next_level_stack = []  

        while stack or next_level_stack:
            if not stack:
                stack, next_level_stack = next_level_stack, []  
                current_depth += 1
                print(f"Proceeding to depth level {current_depth}")
                if current_depth > depth_limit:
                    print("Depth limit reached. Stopping further exploration.")
                    return
            current_node, depth = stack.pop()  

            if current_node not in visited:
                print("Visiting:", current_node)
                self.update_node_color(current_node, COLOR_VISITING) 

                if current_node == goal_node:
                    path = self.reconstruct_path(parents, goal_node)
                    print("Path found:", " -> ".join(path))
                    
                    print("Goal:", current_node)
                    self.update_node_color(current_node, COLOR_GOAL)  
                    self.show_goal_message(goal_node)  
                    return

                visited.add(current_node)
                print("Visited:", current_node)
                self.update_node_color(current_node, COLOR_VISITED) 

                for neighbor in reversed(self.get_neighbors(current_node)):
                    if neighbor not in visited and all(neighbor != n for n, d in stack + next_level_stack):
                        if depth == current_depth:
                            next_level_stack.append((neighbor, depth + 1))  
                        else:
                            stack.append((neighbor, depth + 1))  

                        parents[neighbor] = current_node 
                        print("Adding neighbor:", neighbor, "at depth:", depth + 1)
                        self.update_node_color(neighbor, COLOR_VISITING) 

    def reconstruct_path(self, parents, goal_node):
        path = []
        current_node = goal_node

        while current_node is not None:
            path.append(current_node)
            current_node = parents[current_node]
        
        path.reverse()
        return path
