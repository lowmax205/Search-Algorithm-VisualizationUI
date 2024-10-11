# Color constants
COLOR_VISITED = 'green'
COLOR_VISITING = 'yellow'
COLOR_NOT_VISITED = 'white'
COLOR_GOAL = 'red'

class BaseSearchLogic:
    # Initialize with canvas, functions to update node color and show goal message
    def __init__(self, canvas, update_node_color, show_goal_message):
        self.canvas = canvas  
        self.update_node_color = update_node_color 
        self.show_goal_message = show_goal_message 
        self.node_colors = {}  

    # Set positions for nodes and initialize their colors to 'not visited'
    def set_positions(self, positions):
        self.positions = positions
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.positions}
        
    # Reset all node colors to 'not visited'
    def reset_colors(self, animate=False):
        self.node_colors = {node: COLOR_NOT_VISITED for node in self.node_colors}
        for node in self.node_colors:
            self.update_node_color(node, COLOR_NOT_VISITED)
            
        if animate == True:
            print("All nodes have been reset to 'not visited'.")