from source import COLOR_VISITING, COLOR_GOAL, COLOR_VISITED, reconstruct_path
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

            current_node, depth = current_level.pop(0) 

            if depth > depth_limit: 
                continue
            
            if current_node not in visited:
                print(f"Visiting: {current_node} at depth {depth}")
                self.update_node_color(current_node, COLOR_VISITING)  

                if current_node == goal_node:
                    reconstruct_path(parents, start_node, goal_node, self.node_costs)
                    print(f"Goal node: {current_node}")
                    self.update_node_color(current_node, COLOR_GOAL) 
                    self.show_goal_message(goal_node) 
                    return True

                visited.add(current_node) 
                self.update_node_color(current_node, COLOR_VISITED)

                if depth < depth_limit:  
                    for neighbor in self.get_neighbors(current_node):
                        if neighbor not in visited:
                            next_level.append((neighbor, depth + 1)) 
                            parents[neighbor] = current_node  
                            print(f"Adding Neighbor: {neighbor} at depth {depth + 1}")
        return False
