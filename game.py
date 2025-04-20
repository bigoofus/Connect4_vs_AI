from constants import PLAYER , AI_PLAYER
import random
class Connect4:
    def __init__(self , width = 7 , height = 6):
        self.width = width
        self.height = height
        self.playerTurn = PLAYER         #1 is User and 0 is computer
        self.board = '.' * (self.width * self.height)
        self.game_over = False
        self.winner = None

    def copy(self):
        new_game = Connect4(width = self.width , height = self.height)

        new_game.playerTurn = self.playerTurn
        new_game.board = self.board[:]
        new_game.game_over = self.game_over

        return new_game

    def add_piece(self , col , player):
        if col < 0 or col >= self.width:
            print('Invalid Column: Column out of range')
            return

        if player != self.playerTurn:
            print('Error: Player Mismatch')
            return

        for row in reversed(range(self.height)):
            index = row * self.width + col
            
            if self.board[index] == '.':

                player_turn = str(self.playerTurn)
                self.board = self.board[:index] + player_turn + self.board[index + 1:]
                self.playerTurn =  1 - self.playerTurn

                return row
            
        print('Invalid Column: Column is full')
        return None
    
    def add_piece_exp(self , col , player):
        valid_cols = self.get_valid_columns()

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

        target_col = random.choices(
            list(probs.keys()),
            weights=list(probs.values()),
            k=1
        )[0]

        self.add_piece(target_col , player)

        return None

    def set_slot(self , row , col , value):
        index = row * self.width + col

        self.board = self.board[:index] + value + self.board[index+1:] if index < len(self.board) else self.board

    def get_slot(self , row , col):
        index = row * self.width + col

        return self.board[index] if index < len(self.board) else None
    
    def __str__(self):              #Print visualisation of board
        output = []
        print('\n\n')
        for row in range(self.height):
            start = row * self.width
            end = start + self.width
            output.append('|' + '|'.join(self.board[start:end]) + '|')
        return '\n'.join(output)
    def printboard(self):              #Print visualisation of board
        self.__str__()

    def check_game_over(self):
        if(self.get_valid_columns() == []):
            self.game_over = True
        return self.game_over

    def check_winner(self):
        player_connections = self.count_connect4s(PLAYER)
        comp_connections = self.count_connect4s(AI_PLAYER)

        if(player_connections > comp_connections):
            print('\nPlayer Wins!!')
            self.winner = 1
        elif (player_connections < comp_connections):
            print('\nAI Wins!!')
            self.winner = 0
        else:
            print('\nDraw!!')
            self.winner = -1 #draw

    def count_connect4s(self , player):
        count = 0
        seq = str(player) * 4

        board_str = self.board

        for row in range (self.height):             #Count Horizontal 4s
            row_start = row * self.width
            row_end = row * self.width + self.width
            row_str = board_str[row_start:row_end] 
            count += sum(1 for i in range(len(row_str) - 3) if row_str[i : i + 4] == seq)

        for col in range (self.width):              #Count vertical 4s
            col_str = ''.join([board_str[row * self.width + col] for row in range(self.height)])

            count += sum(1 for i in range(len(row_str) - 3) if col_str[i : i + 4] == seq)

        max_diag_length = min(self.width , self.height)

        for diag in range(-self.height + 1 , self.width):
            diag_str = []
            for row in range(self.height):
                col = diag + row
                if 0 <= col < self.width:
                    diag_str.append(board_str[row * self.width + col])
            diag_str = ''.join(diag_str)
            count += sum(1 for i in range(len(row_str) - 3) if diag_str[i : i + 4] == seq)

        for diag in range(0 , self.width + self.height - 1):
            diag_str = []
            for row in range(self.height):
                col = diag - row
                if 0 <= col < self.width:
                    diag_str.append(board_str[row * self.width + col])
            
            diag_str = ''.join(diag_str)
            count += sum(1 for i in range(len(row_str) - 3) if diag_str[i : i + 4] == seq)

        return count
    
    def get_valid_columns(self):
        return [col for col in range(self.width) if self.get_slot(0, col) == '.']



    def get_next_open_row(self, col):
        for row in reversed(range(self.height)):
            if self.get_slot(row, col) == '.':
                return row
        return None
    
    def is_valid_location(self, col):
        return  self.get_slot(0, col) == '.'
    
    