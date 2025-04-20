from game import Connect4
from constants import AI_PLAYER , PLAYER
from heuristic import compute_heuristic_score

def minimax(game , depth , maximizing_player = True):

    if depth == 0 or game.game_over:
        return compute_heuristic_score(game) , None
    else: 

        valid_cols = game.get_valid_columns()
        best_move = None
    
        if maximizing_player:
            max_score = -float('inf')
            
            for col in valid_cols:
                new_board = game.copy()
                new_board.add_piece(col , AI_PLAYER)
                current_score, _ = minimax(new_board, depth-1, maximizing_player = False)

                if current_score > max_score:
                    max_score = current_score
                    best_move = col

            return max_score, best_move
        
        else:
            min_score = float('inf')
            for col in valid_cols:
                new_board = game.copy()
                new_board.add_piece(col , PLAYER)
                current_score, _ = minimax(new_board, depth-1, maximizing_player = True)
            
                if current_score < min_score:
                    min_score = current_score
                    best_move = col

            return min_score, best_move
        
def minimax_pruning(game , depth , maximizing_player = True , alpha = -float('inf') , beta = float('inf')):

    if depth == 0 or game.game_over:
        return compute_heuristic_score(game) , None
    else: 

        valid_cols = game.get_valid_columns()
        best_move = None
    
        if maximizing_player:
            max_score = -float('inf')
            
            for col in valid_cols:
                new_board = game.copy()
                new_board.add_piece(col , AI_PLAYER)
                current_score, _ = minimax_pruning(new_board, depth-1, maximizing_player = False , alpha = alpha, beta = beta)

                if current_score > max_score:
                    max_score = current_score
                    best_move = col
                
                alpha = max(alpha , max_score)

                if max_score > beta:
                    break

            return max_score, best_move
        
        else:
            min_score = float('inf')
            for col in valid_cols:
                new_board = game.copy()
                new_board.add_piece(col , PLAYER)
                current_score, _ = minimax_pruning(new_board, depth-1, maximizing_player = True , alpha = alpha , beta = beta)
            
                if current_score < min_score:
                    min_score = current_score
                    best_move = col

                beta = min(beta , min_score)

                if min_score < alpha:
                    break

            return min_score, best_move

def expectiminimax(game , depth , maximizing_player = True):
    if depth == 0 or game.game_over:
        return compute_heuristic_score(game) , None
    else:
        valid_cols = game.get_valid_columns()

        if maximizing_player:       #AI's Turn (No probability involved)
            max_score = -float('inf')
            best_move = valid_cols[0]
            
            for col in valid_cols:
                new_board = game.copy()
                new_board.add_piece(col , AI_PLAYER)
                current_score, _ = expectiminimax(new_board, depth-1, maximizing_player = False)

                if current_score > max_score:
                    max_score = current_score
                    best_move = col

            return max_score, best_move
        
        else:       #Player's Turn (Probability Involved)
            expected_score = 0
        best_move = None
        
        for col in valid_cols:
            #possible columns per move and their probabilities

            left_available = (col - 1) in valid_cols
            right_available = (col + 1) in valid_cols
            
            if left_available and right_available:
                probs = {col: 0.6, col-1: 0.2, col+1: 0.2}
            elif left_available:
                probs = {col: 0.6, col-1: 0.4}
            elif right_available:
                probs = {col: 0.6, col+1: 0.4}
            else:
                probs = {col: 1.0}

            col_score = 0

            for move_col, prob in probs.items():
                new_game = game.copy()
                new_game.add_piece(move_col, PLAYER)
                current_score, _ = expectiminimax(new_game, depth-1, True)
                col_score += prob * current_score
            
            if best_move is None or col_score < expected_score:
                expected_score = col_score
                best_move = col
                
        return expected_score, best_move