import tkinter as tk
from constants import AI_PLAYER, PLAYER

class TreeVisualizer:
    def __init__(self, master, root_node):
        self.master = master
        self.master.title("Tree Visualizer")

        # Frame to hold canvas
        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Canvas
        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Arrow keys binding
        self.master.bind("<Left>", lambda e: self.canvas.xview_scroll(-1, "units"))
        self.master.bind("<Right>", lambda e: self.canvas.xview_scroll(1, "units"))
        self.master.bind("<Up>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.master.bind("<Down>", lambda e: self.canvas.yview_scroll(1, "units"))

        # Zoom controls
        self.zoom_factor = 1.0
        self.master.bind('+', lambda event: self.zoom_in())
        self.master.bind('-', lambda event: self.zoom_out())

        self.root = root_node

        self.node_radius = 50
        self.font = ("Tex Gyre Adventor", 12, "bold")
        self.vertical_spacing = 200
        self.horizontal_spacing = 200

        self.calculate_positions(self.root)
        self.draw_static_tree()

    def zoom_in(self):
        self.zoom_factor *= 1.01
        self.update_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.01
        self.update_zoom()

    def update_zoom(self):
        self.canvas.scale('all', 0, 0, self.zoom_factor, self.zoom_factor)

    def calculate_positions(self, node, depth=0, x_offset=0):
        if not node.children:
            node.x = x_offset
            node.y = depth * self.vertical_spacing
            return 1

        width = 0
        child_x = x_offset
        for child in node.children:
            sub_width = self.calculate_positions(child, depth+1, child_x)
            child_x += sub_width * self.horizontal_spacing
            width += sub_width

        node.x = (x_offset + (child_x - self.horizontal_spacing)) / 2
        node.y = depth * self.vertical_spacing
        return width

    def draw_static_tree(self):
        self.canvas.delete('all')
        self._draw_connections(self.root)
        self._draw_nodes(self.root)

        self.master.update()
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.config(scrollregion=bbox)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x_center = (bbox[0] + bbox[2]) // 2
            y_center = (bbox[1] + bbox[3]) // 2
            self.canvas.xview_moveto((x_center - canvas_width // 2) / bbox[2])
            self.canvas.yview_moveto((y_center - canvas_height // 2) / bbox[3])

    def _draw_connections(self, node):
        for child in node.children:
            self.canvas.create_line(
                node.x, node.y + self.node_radius,
                child.x, child.y - self.node_radius,
                fill="black"
            )
            self._draw_connections(child)

    def _draw_nodes(self, node):
        if node.parent and node.parent.get_best_child() == node:
            fill_color = "green"
        elif node.player_turn == PLAYER:
            fill_color = "red"
        elif node.player_turn == AI_PLAYER:
            fill_color = "yellow"
        else:
            fill_color = "lightblue"

        self.canvas.create_oval(
            node.x - self.node_radius, node.y - self.node_radius,
            node.x + self.node_radius, node.y + self.node_radius,
            fill=fill_color, outline="black"
        )

        player_type = f" ({node.player_turn})" if node.player_turn else ""
        node_text = f"{node.move}\nScore: {node.heuristic_score}\n{player_type}"

        self.canvas.create_text(
            node.x, node.y,
            text=node_text,
            font=self.font,
            anchor="center"
        )

        for child in node.children:
            self._draw_nodes(child)
