from constants import AI_PLAYER , PLAYER , EMPTY , WIDTH , HEIGHT


def compute_heuristic_score(game):
    score = 0
    human_open_threes = 0
    computer_open_threes = 0
    human_open_twos = 0
    computer_open_twos = 0
    
    computer_fours = game.count_connect4s(AI_PLAYER)
    human_fours = game.count_connect4s(PLAYER)
    score += (computer_fours - human_fours) * 10000
    
    # Computer's open 3-in-a-rows
    for segment in get_all_segments(game):
        ai_count = segment.count(str(AI_PLAYER))
        human_count = segment.count(str(PLAYER))
        empty_count = segment.count(EMPTY)
        
        # Computer's open three
        if ai_count == 3 and empty_count == 1:
            computer_open_threes += 1
            
        # Human's open three (potential immediate threat)
        if human_count == 3 and empty_count == 1:
            human_open_threes += 1

        # Computer's open twos
        if ai_count == 2 and empty_count == 2:
            computer_open_twos += 1
            
        # Human's open twos
        if human_count == 2 and empty_count == 2:
            human_open_twos += 1

    
    score += computer_open_threes * 5000
    score -= human_open_threes * 10000  # Higher weight for blocking (Defensive Plays)

    score += computer_open_twos * 100
    score -= human_open_twos * 200
    
    # Center Control
    center_cols = {WIDTH // 2 - 1 , WIDTH // 2 , WIDTH // 2 + 1}
    center_control = sum(
        1 for col in center_cols
        for row in range(HEIGHT)
        if game.get_slot(row , col) == AI_PLAYER
    ) - sum(
        1 for col in center_cols
        for row in range(HEIGHT)
        if game.get_slot(row , col) == PLAYER
    )
    score += center_control * 15
    
    # Mobility
    valid_moves = sum(
        1 for col in range(WIDTH)
        if game.get_slot(HEIGHT - 1 , col) == EMPTY  # Check top of column
    )
    score += valid_moves * 2
    
    return score

def get_all_segments(board):
    """Generator for all possible 4-cell segments using get()"""
    # Horizontal
    for row in range(HEIGHT):
        for col in range(WIDTH - 3):
            yield [board.get_slot(row, col+i) for i in range(4)]
    
    # Vertical
    for col in range(WIDTH):
        for row in range(HEIGHT - 3):
            yield [board.get_slot(row+i, col) for i in range(4)]
    
    # Diagonal
    for row in range(HEIGHT - 3):
        for col in range(WIDTH - 3):
            yield [board.get_slot(row+i, col+i) for i in range(4)]       #Positive Slope diagonals
            yield [board.get_slot(row+3-i, col+i) for i in range(4)]     #Negative Slope diagonals