import pygame
import sys
import math
from game import Connect4
from algorithms import *
from constants import *
# from tree import * 
import threading
from tree3 import *
from visulizer import *

import tkinter as tk


def start_game(selected_mode,depth,tree_visualizer):
    # Setup
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    # if tree_visualizer:
    #     create_window((1200, 1000))
    #     # threading.Thread(target=create_window, args=((1200, 1000)), daemon=True).start()
        

    game = Connect4()

    pygame.init()
    screen = pygame.display.set_mode(size)

    font = pygame.font.SysFont("texgyreadventor-bold", 75)

    def draw_board(game):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if game.get_slot(r, c) == "0":
                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif game.get_slot(r, c) == "1":
                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    if selected_mode=="Minimax with Pruning":
        pygame.display.set_caption("Connect 4 vs minimax-pruning AI")
    elif selected_mode=="Minimax without Pruning":
        pygame.display.set_caption("Connect 4 vs minimax-without-pruning AI")
    else:
        pygame.display.set_caption("Connect 4 vs expectiminimax AI")
    turn = PLAYER
    draw_board(game)

    while not game.game_over:
        
        for even in pygame.event.get():
            if even.type == pygame.QUIT:
                sys.exit()

            if even.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = even.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if even.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                if turn == PLAYER:
                    posx = even.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if game.is_valid_location(col):
                        game.add_piece(col, PLAYER)
                    turn = AI_PLAYER
                    print(game)
                    draw_board(game)
                    pygame.display.update()
            if turn == AI_PLAYER and not game.game_over:
                ai_move(selected_mode,game,depth,tree_visualizer)       
                
            
            turn = PLAYER
            draw_board(game)

            state= game.check_game_over()
            if state == True:
                print('Game Over!!')
                game.check_winner()
                winner=game.winner
                if winner == 1:
                    label = font.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    pygame.display.update()
                elif winner == 0:
                    label = font.render("AI wins!!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    pygame.display.update()
                else:
                    label = font.render("Game Draw!!", 1, WHITE)
                    screen.blit(label, (40,10))
                    pygame.display.update()
                pygame.time.wait(3000)
                
                break
    
                            
# def ai_move(selected_mode, game, depth, visualizer):
#     if selected_mode == "Minimax with Pruning":
#         best_score, best_move = minimax_pruning(game, depth, True)
#         game.add_piece(best_move, AI_PLAYER)
#     elif selected_mode == "Minimax without Pruning":
#         min_score, best_move = minimax(game, depth, True)
#         game.add_piece(best_move, AI_PLAYER)
#     else: 
#         expected_score, best_move = expectiminimax(game, depth, True)
#         game.add_piece(best_move, AI_PLAYER)

#     if visualizer:
#         from tree import visualize_tree
#         visualize_tree(game, depth=depth)



# def ai_move(selected_mode, game, depth, visualizer):
#     if selected_mode == "Minimax with Pruning":
#         tree_root,best_move,_ = minimax_pruning_tree(game, depth, maximizing_player=True)
#     elif selected_mode == "Minimax without Pruning":
#         score, root_node = minimax_with_tree(game, depth=3)
#         best_child = root_node.get_best_child()
#         best_move = best_child.move
#         root_node.print_tree()
#         root_node.print_best_child()
#         if visualizer:
#             visualize_tree(root_node)
        
        
        
        
#     else:  
#         tree_root,best_move,_ = expectiminimax_tree(game, depth, maximizing_player=True)

    
    
#     game.add_piece(best_move, AI_PLAYER)




def visualize_tree(root_node):
    """Create a Tkinter window in a thread and visualize the tree."""

    def start_tk():
        root = tk.Tk()
        visualizer = TreeVisualizer(root, root_node=root_node)  # Pass the real root node
        visualizer.calculate_positions(visualizer.root)  # First calculate positions
        visualizer.draw_static_tree()  # Then draw the static tree
        root.mainloop()

    tkinter_thread = threading.Thread(target=start_tk)
    tkinter_thread.daemon = True
    tkinter_thread.start()



def ai_move(selected_mode, game, depth, visualizer):
    if selected_mode == "Minimax with Pruning":
        score, root_node = minimax_pruning_tree(game, depth, maximizing_player=True)
    elif selected_mode == "Minimax without Pruning":
        score, root_node = minimax_with_tree(game, depth)
    else:  
        score, root_node = expectiminimax_tree(game, depth)

    best_child = root_node.get_best_child()
    best_move = best_child.move
    root_node.print_tree()
    root_node.print_best_child()
    if visualizer:
        visualize_tree(root_node)
    game.add_piece(best_move, AI_PLAYER)


    




    

                    







 
 
