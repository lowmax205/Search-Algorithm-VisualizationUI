from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED
from source import BaseSearchLogic

class IDSLogic(BaseSearchLogic):
    def ids(self, start_node, goal_node=None):
        depth = 0
        while True:
            print(f"Exploring with depth limit: {depth}")
            found = self.dls(start_node, goal_node, depth) 
            if found:
                return  
            depth += 1  
            self.reset_colors()  

    def dls(self, start_node, goal_node, depth_limit):
        current_level = [(start_node, 0)] 
        next_level = [] 
        visited = set() 
        parents = {start_node: None} 

        while current_level or next_level:
            if not current_level:
                current_level, next_level = next_level, []
                if current_level:
                    print(f"Proceeding to depth level: {current_level[0][1]}")

            node, depth = current_level.pop(0) 

            if depth > depth_limit: 
                continue
            
            if node not in visited:
                print(f"Visiting: {node} at depth {depth}")
                self.update_node_color(node, COLOR_VISITING)  

                if node == goal_node: 
                    path = self.reconstruct_path(parents, goal_node)
                    print("Path found:", " -> ".join(path))
                    
                    print(f"Goal: {node} reached.")
                    self.update_node_color(node, COLOR_GOAL)
                    self.show_goal_message(goal_node)
                    return True

                visited.add(node) 
                self.update_node_color(node, COLOR_VISITED)

                if depth < depth_limit:  
                    for neighbor in self.get_neighbors(node):
                        if neighbor not in visited:
                            next_level.append((neighbor, depth + 1)) 
                            parents[neighbor] = node  
                            print(f"Adding Neighbor: {neighbor} at depth {depth + 1}")
        return False

    def reconstruct_path(self, parents, goal_node):
        path = []
        current_node = goal_node

        while current_node is not None:
            path.append(current_node)
            current_node = parents[current_node] 
        
        path.reverse() 
        return path
