# Followed https://github.com/KeithGalli/Connect4-Python/blob/503c0b4807001e7ea43a039cb234a4e55c4b226c/connect4_with_ai.py

import numpy as np
import random
import sys
import math
from colored import fg, style
import os

ROW_COUNT = 6
COLUMN_COUNT = 7

playerColors = ("1", "4")
playerTokens = ("X", "O")

aiPlayers = (0, 1)
aiDepth =   (5, 5)

emptyToken = 0

currentPlayer = 1

WINDOW_LENGTH = 4

def other_player(currentPlayer):
    """
    Simply returns the "other" player piece
    1 -> 2
    2 -> 1
    """
    return 1 if currentPlayer == 2 else 2

def create_board():
    """
    Generates a empty board array with numpy and returns it
    """
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_column_not_full(board, col):
    """
    Returns True if the selected column has atleast one free slot at the top.
    Returns False if there is no more slots on that column.
    """
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    """
    Gets the next free slot on the selected column.
    Returns False if the column is full.
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    return False

def print_board(board):
    screenMatrix = np.flip(board, 0)

    topBorder = ["▁", (COLUMN_COUNT * 2) + 1]
    bottomBorder = ["▔", topBorder[1]]
    sideBorder = "│"

    # os.system('cls')

    print(topBorder[0] * topBorder[1])

    for rows in screenMatrix:

        printRow = []
        for item in rows:
            if item == emptyToken:
                printRow.append(" ")
            elif item == 1:
                printRow.append(fg(playerColors[0]) + playerTokens[0] + style.RESET)
            elif item == 2:
                printRow.append(fg(playerColors[1]) + playerTokens[1] + style.RESET)
            else:
                printRow.append(item)

        print(sideBorder + sideBorder.join(printRow) + sideBorder)

    print(bottomBorder[0] * bottomBorder[1])

def winning_move(board, piece):
    """
    Returns True if the current piece has won on this board
    Returns False if the current piece has not won on this board
    """
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False

def evaluate_window(window, piece):
    score = 0

    opp_piece = other_player(piece)

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(emptyToken) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(emptyToken) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(emptyToken) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    """
    Returns True if;\n
    * Player 1 can win on this board
    * Player 2 can win on this board
    * All the slots are filled on this board (Tie)
    """
    return winning_move(board, currentPlayer) or winning_move(board, other_player(currentPlayer)) or len(get_valid_columns(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_columns(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, currentPlayer):
				return (None, 100000000000000)
			elif winning_move(board, other_player(currentPlayer)):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, currentPlayer))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, currentPlayer)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, other_player(currentPlayer))
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_columns(board):
    """
    Returns all the column indexes that are not full\n
    [0, 1, 2, 3, 4, 5, 6]
    """
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_column_not_full(board, col):
            valid_locations.append(col)
    return valid_locations

def can_i_win(board, piece):
    """
    Returns {col, row} if the selected piece could win with one move.
    The col and row is the position to place the piece in order to win

    If the selected piece can not win with one move, it returns False
    """
    valid_columns = get_valid_columns(board)

    for col in valid_columns:
        b_copy = board.copy()
        row = get_next_open_row(b_copy, col)
        drop_piece(b_copy, row, col, piece)

        win_status = winning_move(b_copy, piece)
        if win_status:
            return {
                "col": col,
                "row": row
            }

    return False

board = create_board()
print_board(board)

while 1:
    if aiPlayers[currentPlayer-1]:
        # AI PLAYER TURN
        print(f"Loading AI player {currentPlayer}'s move...")

        can_i_win_return = can_i_win(board, currentPlayer)
        can_the_other_player_win_return = can_i_win(board, other_player(currentPlayer))

        # If the current player can win with one move, then it always makes sure to place that
        if can_i_win_return != False:  
            drop_piece(board, can_i_win_return['row'], can_i_win_return['col'], currentPlayer)
        
        # If the other player can win with one move, then it always makes sure to block that
        elif can_the_other_player_win_return != False:
            drop_piece(board, can_the_other_player_win_return['row'], can_the_other_player_win_return['col'], currentPlayer)
        
        # If none of the above, go back to default AI Behaviour
        else:
            col, minimax_score = minimax(board, aiDepth[currentPlayer-1], -math.inf, math.inf, True)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, currentPlayer)
        # col, minimax_score = minimax(board, aiDepth[currentPlayer-1], -math.inf, math.inf, True)
        # row = get_next_open_row(board, col)
        # drop_piece(board, row, col, currentPlayer)
    else:
        # HUMAN PLAYER TURN
        playerSelection = input("Player %s, välj rad : " % currentPlayer)

        try:
            playerSelection = int(playerSelection)
        except Exception:
            print_board(board)
            print("Not good input")
            continue
        if playerSelection < 1 or playerSelection > COLUMN_COUNT:
            print_board(board)
            print("Out of bounds")
            continue

        col = playerSelection - 1

        if is_column_not_full(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, currentPlayer)
        else:
            print_board(board)
            print("Column is full")
            continue

    # AFTER MOVE STUFF
    print_board(board)

    if winning_move(board, currentPlayer):
        print(f"PLAYER {currentPlayer} WINS")
        exit()

    currentPlayer = other_player(currentPlayer) # Switch player turn