import tkinter as tk

class Node:
    def __init__(self, move, parent=None, children=None, heuristic_score=None, player_turn=None):
        self.move = move
        self.parent = parent
        self.children = children if children is not None else []
        self.heuristic_score = heuristic_score
        self.player_turn = player_turn
        self.best_child = None

    def addchild(self, child):
        self.children.append(child)

    def addparent(self, parent):
        self.parent = parent

    def add_best_child(self, best_child):
        self.best_child = best_child

    def get_best_child(self):
        return self.best_child

    def print_best_child(self):
        if self.best_child is not None:
            print(f"Best child move: {self.best_child.move}, Score: {self.best_child.heuristic_score}")
        else:
            print("No best child found.")

    def print_tree(self, level=0):
        indent = "    " * level
        print(f"{indent}Move: {self.move}, Score: {self.heuristic_score}, Player: {self.player_turn}")
        for child in self.children:
            child.print_tree(level + 1)
