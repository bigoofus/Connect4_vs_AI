import tkinter as tk
import threading
from heuristic import compute_heuristic_score
from constants import AI_PLAYER, PLAYER

canvas = None
root = None
scroll_x = None
scroll_y = None

# Constants
NODE_RADIUS = 40
EDGE_OFFSET = 10
HORIZONTAL_SPACING = NODE_RADIUS * 6
VERTICAL_SPACING = NODE_RADIUS * 6
TEXT_FONT = ("TexGyreAdventor-Bold", 14)

# Save last tree to redraw on resize
_last_tree = None

# Colors
DEFAULT_NODE_COLOR = "lightblue"
BEST_NODE_COLOR = "lightgreen"
EDGE_COLOR = "black"
BEST_EDGE_COLOR = "green"

def create_window(size):
    def run_tkinter():
        global canvas, root, scroll_x, scroll_y
        root = tk.Tk()
        root.title("Tree Visualizer")
        root.geometry(f"{size[0]}x{size[1]}")

        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame, bg="white")
        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        hbar.config(command=canvas.xview)
        vbar.config(command=canvas.yview)

        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.bind("<Configure>", on_canvas_resize)

        scroll_x = hbar
        scroll_y = vbar

        root.mainloop()

    threading.Thread(target=run_tkinter, daemon=True).start()

def clear_canvas():
    if canvas:
        canvas.delete("all")

def on_canvas_resize(event):
    if _last_tree:
        draw_full_tree(_last_tree)

def draw_node(x, y, text, color=DEFAULT_NODE_COLOR):
    if canvas:
        canvas.create_oval(x-NODE_RADIUS, y-NODE_RADIUS, x+NODE_RADIUS, y+NODE_RADIUS, fill=color, outline="black")
        canvas.create_text(x, y, text=text, font=TEXT_FONT)

def draw_edge(x1, y1, x2, y2, color=EDGE_COLOR):
    if canvas:
        canvas.create_line(x1, y1 + NODE_RADIUS + EDGE_OFFSET, x2, y2 - NODE_RADIUS - EDGE_OFFSET, fill=color)

class TreeNode:
    def __init__(self, move=None, heuristic=0, player_turn=AI_PLAYER):
        self.move = move
        self.heuristic = heuristic
        self.player_turn = player_turn  # <--- NEW!
        self.children = []
        self.best = False


def build_tree(game, depth):
    root = TreeNode(move=None, heuristic=compute_heuristic_score(game))
    build_subtree(root, game, depth)
    return root

def build_subtree(node, game, depth):
    if depth == 0 or game.check_game_over():
        return

    for col in game.get_valid_columns():
        child_game = game.copy()

        if depth % 2 != 0:
            child_game.turn = AI_PLAYER
            next_player_turn = PLAYER
        else:
            child_game.turn = PLAYER
            next_player_turn = AI_PLAYER

        child_game.add_piece(col, child_game.playerTurn)
        child_node = TreeNode(move=col, heuristic=compute_heuristic_score(child_game), player_turn=next_player_turn)
        node.children.append(child_node)
        build_subtree(child_node, child_game, depth-1)


def assign_positions(node, x=0, y=0, level_spacing=VERTICAL_SPACING):
    if not hasattr(node, 'pos'):
        node.pos = (0, 0)

    if not node.children:
        node.pos = (x, y)
        return x + NODE_RADIUS * 4

    start_x = x
    for child in node.children:
        x = assign_positions(child, x, y + level_spacing)

    # Center parent above its children
    first_child_x, _ = node.children[0].pos
    last_child_x, _ = node.children[-1].pos
    node_x = (first_child_x + last_child_x) // 2
    node.pos = (node_x, y)

    return x

def draw_assigned_tree(node):
    x, y = node.pos

    if node.best:
        node_color = BEST_NODE_COLOR
    elif node.player_turn == PLAYER:
        node_color = "red"  # <--- Red if it's PLAYER's turn
    else:
        node_color = DEFAULT_NODE_COLOR

    draw_node(x, y, f"{node.move}\n{node.heuristic}", color=node_color)

    for child in node.children:
        child_x, child_y = child.pos
        edge_color = BEST_EDGE_COLOR if child.best else EDGE_COLOR
        draw_edge(x, y, child_x, child_y, color=edge_color)
        draw_assigned_tree(child)


def find_min_x(node):
    min_x, _ = node.pos
    for child in node.children:
        min_x = min(min_x, find_min_x(child))
    return min_x

def find_max_x(node):
    max_x, _ = node.pos
    for child in node.children:
        max_x = max(max_x, find_max_x(child))
    return max_x

def find_max_y(node):
    max_y = node.pos[1]
    for child in node.children:
        max_y = max(max_y, find_max_y(child))
    return max_y

def shift_positions(node, dx, dy):
    x, y = node.pos
    node.pos = (x + dx, y + dy)
    for child in node.children:
        shift_positions(child, dx, dy)

def highlight_best_move(root):
    def dfs(node, path):
        if not node.children:
            # Leaf node
            return (node.heuristic, path + [node])
        best_score = float('-inf')
        best_path = []
        for child in node.children:
            score, child_path = dfs(child, path + [node])
            if score > best_score:
                best_score = score
                best_path = child_path
        return best_score, best_path

    # Perform DFS to find best path
    _, best_path = dfs(root, [])

    # Mark all nodes in the best path
    for node in best_path:
        node.best = True

def draw_full_tree(tree_root):
    clear_canvas()
    if canvas:
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        assign_positions(tree_root, x=NODE_RADIUS * 2, y=50)

        min_x = find_min_x(tree_root)
        max_x = find_max_x(tree_root)
        max_y = find_max_y(tree_root)

        extra_margin_x = 300
        extra_margin_y = 300

        total_tree_width = max_x - min_x + 2 * extra_margin_x
        total_tree_height = max_y + extra_margin_y

        # Shift everything to right and down
        shift_positions(tree_root, extra_margin_x - min_x, 50)

        # Set scroll region
        canvas.config(scrollregion=(-extra_margin_x, 0, total_tree_width, total_tree_height))

        # Highlight the best move at the root level
        highlight_best_move(tree_root)

        draw_assigned_tree(tree_root)

def visualize_tree(game, depth):
    global _last_tree
    _last_tree = build_tree(game, depth)
    draw_full_tree(_last_tree)
