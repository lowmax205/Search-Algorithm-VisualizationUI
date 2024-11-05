from source import COLOR_START, COLOR_VISITED, COLOR_VISITING, COLOR_GOAL
from source import BaseSearchLogic
import heapq

class AStarLogic(BaseSearchLogic):
    def __init__(self, canvas, update_node_color, show_goal_message, node_lines):
        super().__init__(canvas, update_node_color, show_goal_message, node_lines)
        self.node_lines = self.node_lines
        self.positions_star = {}
        self.edges = [
            ('S', 'N'), ('N', 'S'), ('S', 'Q'), ('Q', 'S'), ('S', 'T'), ('T', 'S'), ('S', 'E'), ('E', 'S'),
            ('N', 'J'), ('J', 'N'),
            ('J', 'I'), ('I', 'J'),
            ('U', 'A'), ('A', 'U'), ('U', 'L'), ('L', 'U'), ('U', 'I'), ('I', 'U'),
            ('Q', 'U'), ('U', 'Q'),
            ('T', 'Q'), ('Q', 'T'), ('T', 'L'), ('L', 'T'),
            ('L', 'B'), ('B', 'L'),
            ('B', 'H'), ('H', 'B'),
            ('H', 'D'), ('D', 'H'),
            ('D', 'R'), ('R', 'D'),
            ('R', 'E'), ('E', 'R'),
            ('E', 'G'), ('G', 'E'), ('E', 'F'), ('F', 'E'), ('E', 'K'), ('K', 'E'),
            ('F', 'M'), ('M', 'F'), ('F', 'O'), ('O', 'F'),
            ('M', 'P'), ('P', 'M'),
            ('K', 'O'), ('O', 'K'),
            ('P', 'C'), ('C', 'P'),
            ('O', 'C'), ('C', 'O')
        ]

        self.SURIGAO_DEL_NORTE_DISTANCE = {
            'A': 46.3, 'B': 38.7, 'C': 104, 'D': 55.1, 'E': 65.2, 
            'F': 87.3, 'G': 80.4, 'H': 52.7, 'I': 36.1, 'J': 30.9, 
            'K': 90.70, 'L': 31.8, 'M': 94.2, 'N': 10.6, 'O': 93.5, 
            'P': 102, 'Q': 19.3, 'R': 95.7, 'S': 0, 'T': 23.5, 'U': 35.2
        }

        self.SURIGAO_DEL_NORTE_COST = {
            'A': 37.57, 'B': 25.95, 'C': 68.45, 'D': 35.67, 'E': 61.45, 
            'F': 54.70, 'G': 72.12, 'H': 21.20, 'I': 28.06, 'J': 21.70, 
            'K': 67.00, 'L': 19.16, 'M': 59.33, 'N': 7.98, 'O': 67.00, 
            'P': 64.70, 'Q': 15.30, 'R': 52.22, 'S': 0, 'T': 14.35, 'U': 27.67
        }

    def astar(self, start_node, goal_node):
        self.update_node_color(goal_node, COLOR_GOAL)
        self.update_node_color(start_node, COLOR_START)
        open_list = [(0, start_node)]
        closed_set = set()
        g_score = {start_node: 0}
        f_score = {start_node: self.heuristic(start_node, goal_node)}
        came_from = {}

        print(f"Starting A* search from {start_node} to {goal_node}")
        print(f"Initial node {start_node}: g(n) = 0, h(n) = {self.heuristic(start_node, goal_node):.2f}, f(n) = {f_score[start_node]:.2f}")

        while open_list:
            current_f, current_node = heapq.heappop(open_list)
            
            if current_node == goal_node:
                path = self.reconstruct_path(came_from, start_node, goal_node)
                self.highlight_path(path, start_node, goal_node)
                total_cost = g_score[goal_node]
                total_distance = sum(self.SURIGAO_DEL_NORTE_DISTANCE[node] for node in path)
                print(f"\nStarting Node: {start_node}")
                print("Path found:", " -> ".join(path))
                print(f"Reached goal: {goal_node}")
                print(f"Total cost: {total_cost:.2f}")
                print(f"Total distance: {total_distance:.2f}")
                self.show_goal_message(f"Goal reached {goal_node}! Total cost: {total_cost:.2f}, Total distance: {total_distance:.2f}")
                return path

            closed_set.add(current_node)
            if current_node != start_node and current_node != goal_node:
                self.update_node_color(current_node, COLOR_VISITED)

            print(f"\nExpanding node {current_node}")
            for neighbor in self.get_neighbors(current_node):
                if neighbor in closed_set:
                    continue

                tentative_g_score = g_score[current_node] + self.SURIGAO_DEL_NORTE_COST[neighbor]

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    h_score = self.heuristic(neighbor, goal_node)
                    f_score[neighbor] = g_score[neighbor] + h_score

                    print(f"  Neighbor {neighbor}:")
                    print(f"    g(n) = {g_score[neighbor]:.2f}")
                    print(f"    h(n) = {h_score:.2f}")
                    print(f"    f(n) = g(n) + h(n) = {g_score[neighbor]:.2f} + {h_score:.2f} = {f_score[neighbor]:.2f}")

                    if neighbor not in [i[1] for i in open_list]:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))
                        
                    if neighbor != start_node and neighbor != goal_node:
                        self.update_node_color(neighbor, COLOR_VISITING)

        print("Goal not reachable")
        return None

    def heuristic(self, node, goal):
        return self.SURIGAO_DEL_NORTE_DISTANCE[node]

    def get_neighbors(self, node):
        return [neighbor for edge in self.edges if edge[0] == node or edge[1] == node for neighbor in edge if neighbor != node]

    def reconstruct_path(self, came_from, start, goal):
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path
