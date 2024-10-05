import tkinter as tk
from tkinter import Canvas

def draw_graph(canvas):
    # Coordinates for the circles (x, y) and corresponding labels
    nodes = {
        'A': (50, 300), 'B': (100, 250), 'C': (200, 200), 
        'D': (300, 250), 'E': (350, 300), 'F': (400, 350),
        'G': (300, 400), 'H': (200, 450), 'I': (100, 400),
        'J': (150, 100), 'K': (250, 150), 'L': (350, 100), 
        'M': (450, 150), 'N': (400, 50)
    }

    # Define the connections (lines between nodes)
    connections = [
        ('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'),
        ('E', 'F'), ('F', 'G'), ('G', 'H'), ('H', 'I'),
        ('I', 'A'), ('C', 'J'), ('J', 'K'), ('K', 'L'),
        ('L', 'M'), ('M', 'N'), ('N', 'L')
    ]

    # Draw lines
    for start, end in connections:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        canvas.create_line(x1, y1, x2, y2, fill="black", width=2)

    # Draw circles and labels
    for label, (x, y) in nodes.items():
        canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="white", outline="black", width=2)
        canvas.create_text(x, y, text=label, font=('Helvetica', 14))

def display_node_list(frame, nodes):
    label = tk.Label(frame, text="Node List", font=('Helvetica', 14))
    label.pack()

    for node in nodes:
        lbl = tk.Label(frame, text=node, font=('Helvetica', 12))
        lbl.pack()

# Create the Tkinter window
window = tk.Tk()
window.title("Graph Layout")

# Create a canvas to draw the graph
canvas = Canvas(window, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT)

# Draw the graph on the canvas
draw_graph(canvas)

# Create a frame for the node list
frame = tk.Frame(window)
frame.pack(side=tk.RIGHT, fill=tk.Y)

# Display the node list
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
display_node_list(frame, nodes)

# Start the Tkinter event loop
window.mainloop()
