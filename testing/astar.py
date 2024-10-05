from queue import PriorityQueue
from source import SURIGAO_DEL_NORTE_DISTANCE as costs, ORIGINAL_HEURISTICS as heuristics
from source import BaseSearchLogic

class AStarLogic(BaseSearchLogic):
    def astar(self, start_node, goal_node):
        open_list = PriorityQueue()
        open_list.put((0, start_node))
        came_from = {}
        g_score = {node: float('inf') for node in self.positions}
        g_score[start_node] = 0

        while not open_list.empty():
            current_f, current_node = open_list.get()
            
            self.update_node_color(current_node, 'yellow')
            if current_node == goal_node:
                self.show_goal_message(goal_node)
                self.reconstruct_path(came_from, start_node, goal_node)
                return
            
            self.update_node_color(current_node, 'green')
            
            for neighbor, cost in self.ucs_get_neighbors(current_node):
                tentative_g_score = g_score[current_node] + cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score = g_score[neighbor] + heuristics.get(neighbor, float('inf'))
                    open_list.put((f_score, neighbor))
        
        return None

    def reconstruct_path(self, came_from, start_node, goal_node):
        current = goal_node
        while current in came_from:
            current = came_from[current]
            self.update_node_color(current, 'blue', animate=True)
