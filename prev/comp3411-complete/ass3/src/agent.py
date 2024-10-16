#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

#################################################################
## QUESTION ANSWER ##############################################
#################################################################
## DATA STRUCTURES:
# * Mark enum:
#   Provides a readable encoding of a possible value for a tic-tac-toe board cell
# * Score enum:
#   Encodes a value to assign to a particular metric that's used in computing a static evaluation score.
#   In descending order of value:
#     - END indicates victory and is assigned the highest value to encourage agent to win.
#     - TOTAL_WINS is if player is winning more overall boards than the opponent.
#     - SINGLE_BOARD_WIN is if player and opponent share same number of overall board wins but player wins current board.
#     - SECOND_BOARD_WIN is if both player and opponent winning current board, but player does so with less moves.
#     - MARK_COUNT_WIN is assigned if neither player or opponent winning current board, but player has less marks in board
#     - NEUTRAL is if the current board is not advantageous to either player
# * Move class:
#   Encodes a move on the entire ultimate tic-tac-toe board.
# * global_grid:
#   A 1D array representing the entire ultimate tic-tac-toe board. 
#   Each slot is given a value from the Mark enum.

# ## PROGRAM:
#   To determine what move to make, minimax is used.
#   Alpha-beta pruning is employed to allow for deeper searches.
#   The minimax algorithm will stop at MAX_DEPTH variable value to ensure search depth is computationally feasible.
#   For each iteration of minimax, all possible moves for the active board are generated.
#   A possible move is one where that cell is empty on the current board.
#   For each move, first check if it has won for the player or opponent and return the END score value relative to depth.
#   This ensures winning at earlier depths are prioritised.
#   Next check if the resulting next board gives the opponent the ability to win.
#   This effectively increase search depth by 1. Assign this an END score if true.
#   Otherwise recurse on minimax for this move.
#   Only at depth 0, i.e. the first iteration of minimax is the move appended to the score.
#   This is because we only want to initial move to be played, not any of the sub-moves whose state are used to calculate the score.
#   If maximising, then take maximum of all scores for this tree depth, otherwise minimum.
#   If at MAX_DEPTH a static evaluation is performed on the board state.
#   Based on the optimal move returned by minimax, a mark is placed on the board.
#   When a mark is placed, the global_active_board_num variable is updated to the cell number chosen.
# ## EVALUATION:
#   For the player to win, the opponent has to put the player in a board where they're 1 mark away from winning.
#   Therefore, it's advantageous for the player to create boards that they're 1 mark away from winning.
#   This is defined in the program as a 'can win'.
#   Firstly, the number of 'can wins' for each board are calculated.
#   If the player and opponent have the same number of 'can wins' for a board, go to one who used less marks.
#   The best case is if the player is winning more overall boards than the opponent. 
#   Assign a multiple of the boards won to the score to prioritise positions where more boards are won.
#   If the player and opponent are winning the same number of boards, look at the current board to distinguish.
#   Based on the desirability of the current board, assign a score according to the Score enum fields.
#   The static evaluation function is symmetric, meaning its run equally for both players. 
#   This ensures each move takes into account other player.

import sys
import socket

from dataclasses import dataclass
from typing import List
from enum import Enum

class Mark(Enum):
  EMPTY = 0
  PLAYER = 1
  OPPONENT = 2

class Score(Enum):
  END = 1000
  TOTAL_WINS = 50
  SINGLE_BOARD_WIN = 40
  SECOND_BOARD_WIN = 30
  MARK_COUNT_WIN = 20
  NEUTRAL = 10
  DRAW = 0
  MAX_SCORE = 10000000
  MIN_SCORE = -MAX_SCORE

@dataclass
class Move:
  board_num: int = 0
  cell_num: int = 0
  score: int = 0

global_num_cells = 9 # width
global_num_boards = 9 # height
global_grid = [Mark.EMPTY] * global_num_cells * global_num_boards
global_next_board_num = 0

def grid_coord(board_num, cell_num):
  global global_num_cells
  return (board_num - 1) * global_num_cells + (cell_num - 1)

def place_mark(board_num, cell_num, mark):
  global global_next_board_num
  global global_grid

  coord = grid_coord(board_num, cell_num)

  global_grid[coord] = mark
  
  global_next_board_num = cell_num

def have_won(grid, cur_board_num, are_max):
  mark = Mark.PLAYER if are_max else Mark.OPPONENT

  active_board_coord = grid_coord(cur_board_num, 1)
  active_board = grid[active_board_coord:active_board_coord+9]

  # 0 1 2
  # 3 4 5
  # 6 7 8
  left_col = (active_board[0] == mark and active_board[3] == mark and active_board[6] == mark)
  middle_col = (active_board[1] == mark and active_board[4] == mark and active_board[7] == mark)
  right_col = (active_board[2] == mark and active_board[5] == mark and active_board[8] == mark)
  top_row = (active_board[0] == mark and active_board[1] == mark and active_board[2] == mark)
  middle_row = (active_board[3] == mark and active_board[4] == mark and active_board[5] == mark)
  bottom_row = (active_board[6] == mark and active_board[7] == mark and active_board[8] == mark)
  left_diag = (active_board[0] == mark and active_board[4] == mark and active_board[8] == mark)
  right_diag = (active_board[6] == mark and active_board[4] == mark and active_board[2] == mark)

  return (left_col or middle_col or right_col or top_row or middle_row or bottom_row or left_diag or right_diag)

def count_can_wins(board, are_max):
  can_wins = 0

  m = Mark.PLAYER if are_max else Mark.OPPONENT

  row_indices = [[0,1,2],[0,2,1],[1,2,0],
                 [3,4,5],[3,5,4],[4,5,3],
                 [6,7,8],[6,8,7],[7,8,6]]
  col_indices = [[0,3,6],[3,6,0],[0,6,3],
                 [1,4,7],[4,7,1],[1,7,4],
                 [2,5,8],[5,8,2],[2,8,5]]
  diag_indices = [[0,4,8],[4,8,0],[0,8,4],
                  [6,4,2],[6,2,4],[4,2,6]]
  for direction_indices in [row_indices, col_indices, diag_indices]:
    for indices in direction_indices:
      i, j, k = indices
      if board[i] == board[j] and board[k] == Mark.EMPTY:
        if board[i] == m:
          can_wins += 1

  return can_wins


def can_win(board, are_max):
  m = Mark.PLAYER if are_max else Mark.OPPONENT

  row_indices = [[0,1,2],[0,2,1],[1,2,0],
                 [3,4,5],[3,5,4],[4,5,3],
                 [6,7,8],[6,8,7],[7,8,6]]
  col_indices = [[0,3,6],[3,6,0],[0,6,3],
                 [1,4,7],[4,7,1],[1,7,4],
                 [2,5,8],[5,8,2],[2,8,5]]
  diag_indices = [[0,4,8],[4,8,0],[0,8,4],
                  [6,4,2],[6,2,4],[4,2,6]]
  for direction_indices in [row_indices, col_indices, diag_indices]:
    for indices in direction_indices:
      i, j, k = indices
      if board[i] == board[j] and board[k] == Mark.EMPTY:
        if board[i] == m:
          return True, k

  return False, -1

MAX_DEPTH = 6

def get_counts(b):
  p = 0
  o = 0
  e = 0
  for i in range(9):
    if b[i] == Mark.PLAYER:
      p += 1
    elif b[i] == Mark.OPPONENT:
      o += 1
    else:
      e += 1

  return [p, o, e]

def static_evaluation(grid, prev_move, are_max):
  # First evaluate entire ultimate tic-tac-toe board and see how many the player is winning
  p_total_wins = 0
  o_total_wins = 0
  
  for i in range(1, 10):
    c = grid_coord(i, 1)
    b = grid[c:c+9]
    p_can_wins = count_can_wins(b, True)
    o_can_wins = count_can_wins(b, False)
    p, o, e = get_counts(b)

    if o == 0:
      # We should've won. This means not placing correctly
      if p == 3:
        return -Score.END.value
      elif p == 1: 
        p_total_wins += 1
      elif p == 2:
        if p_can_wins == 1:
          p_total_wins += 1
        # We should have at least 1 can win. This means not placing correctly
        else:
          return -Score.END.value
      else:
        o_total_wins += 1
    elif p == 0:
      if o == 3:
        return Score.END.value
      elif o == 1: 
        o_total_wins += 1
      elif o == 2:
        if o_can_wins == 1:
          o_total_wins += 1
        else:
          return Score.END.value
    elif p_can_wins > 0 and o_can_wins > 0:
      # If player did it with less marks, better.
      # Any more marks are wasted on this board.
      if p < o: 
        p_total_wins += 1
      elif o < p:
        o_total_wins += 1
    elif p_can_wins > 0:
      p_total_wins += 1
    elif o_can_wins > 0:
      o_total_wins += 1
    elif p < o:
      p_total_wins += 1
    elif p > o:
      o_total_wins += 1

  if o_total_wins > p_total_wins:
    # More total wins the better
    mult = (o_total_wins - p_total_wins)
    return -(mult * Score.TOTAL_WINS.value)
  elif p_total_wins > o_total_wins:
    mult = (p_total_wins - o_total_wins)
    return (mult * Score.TOTAL_WINS.value)
  else:
    # Same number of total wins.
    # So, evaluate the current board to differentiate.
    c = grid_coord(prev_move.board_num, 1)
    b = grid[c:c+9]
    p_wins = count_can_wins(b, True)
    o_wins = count_can_wins(b, False)
    p, o, e = get_counts(b)
    if o == 0:
      if p == 1 or (p == 2 and p_wins == 1):
        return Score.SINGLE_BOARD_WIN.value
      else:
        return -Score.SINGLE_BOARD_WIN.value
    elif p == 0:
      if o == 1 or (o == 2 and o_wins == 1):
        return -Score.SINGLE_BOARD_WIN.value
      else:
        return Score.SINGLE_BOARD_WIN.value
    elif p_wins > 0 and o_wins > 0:
      if p < o:
        return Score.SECOND_BOARD_WIN.value
      elif o < p:
        return -Score.SECOND_BOARD_WIN.value
      else:
        # Both can win, same letter count
        if are_max:
          return Score.NEUTRAL.value
        else:
          return -Score.NEUTRAL.value
    elif p_wins > 0:
      return Score.SINGLE_BOARD_WIN.value
    elif o_wins > 0:
      return -Score.SINGLE_BOARD_WIN.value
    elif p < o:
      return Score.MARK_COUNT_WIN.value
    elif o < p:
      return -Score.MARK_COUNT_WIN.value
    else:
      if are_max:
        return Score.NEUTRAL.value
      else:
        return -Score.NEUTRAL.value

def minimax(grid, depth, are_max, cur_board_num, a, b, prev_move):
  if depth == MAX_DEPTH:
    return static_evaluation(grid, prev_move, are_max)

  scores = []

  possible_moves = get_possible_moves(grid, cur_board_num, are_max)

  for move in possible_moves:
    score = 0
    do_move(grid, move, are_max) 
    if have_won(grid, cur_board_num, True):
      score = Score.END.value - depth
    elif have_won(grid, cur_board_num, False):
      score = depth - Score.END.value
    else:
      next_board_coord = grid_coord(move.cell_num, 1)
      next_board = grid[next_board_coord:next_board_coord+9]
      if can_win(next_board, not are_max)[0]:
        if are_max:
          score = depth -Score.END.value
        else:
          score = Score.END.value - depth
      else:
        score = minimax(grid, depth+1, not are_max, move.cell_num, a, b, move)

    undo_move(grid, move)

    if are_max:
      a = max(a, score)
    else:
      b = min(b, score)

    if b <= a:
      break

    if depth == 0:
      move.score = score
      scores.append([move, score])
    else:
      scores.append(score)

  # If a draw
  if len(scores) == 0:
    return Score.DRAW.value

  if depth == 0:
    if are_max:
      return max(scores, key=lambda x: x[1])[0]
    else:
      return min(scores, key=lambda x: x[1])[0]
  else:
    if are_max:
      return max(scores)
    else:
      return min(scores)

def get_possible_moves(grid, board_num, are_max):
  moves = []
  coord = grid_coord(board_num, 1)
  board = grid[coord:coord+9]

  # 0 1 2
  # 3 4 5
  # 6 7 8
  # Try to place better moves first to aid pruning, i.e. centre then edges
  numbers = [4,0,2,6,8,1,5,7,3]

  for i in numbers:
    if board[i] == Mark.EMPTY:
      move = Move(board_num, i+1, 0)
      moves.append(move)
  return moves

def do_move(grid, move, are_max):
  mark = Mark.PLAYER if are_max else Mark.OPPONENT
  coord = grid_coord(move.board_num, move.cell_num) 
  grid[coord] = mark 

def undo_move(grid, move):
  coord = grid_coord(move.board_num, move.cell_num) 
  grid[coord] = Mark.EMPTY 

def make_move():
  global global_grid
  global global_next_board_num 

  board_coord = grid_coord(global_next_board_num, 1)
  board = global_grid[board_coord:board_coord+9]

  best_move = None

  w, i = can_win(board, True)
  # If can win, win to reduce search time of minimax
  if w:
    best_move = Move(global_next_board_num, i+1, 0)

  if best_move is None:
    best_move = minimax(global_grid, 0, True, global_next_board_num, Score.MIN_SCORE.value, Score.MAX_SCORE.value, None)

  place_mark(global_next_board_num, best_move.cell_num, Mark.PLAYER)

  return best_move.cell_num


def parse_cmd(cmd):
  if "(" in cmd:
    command, args = cmd.split("(")
    args = args.split(")")[0]
    args = args.split(",")
  else:
    command, args = cmd, []

  if command == "init":
    return 0
  elif command == "second_move":
    # Going second, i.e. 'o'
    opponent_board_num = int(args[0])
    opponent_cell_num = int(args[1])

    # Place server generated random move for opponent
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "third_move":
    # Going first, i.e. 'x'
    our_random_board_num = int(args[0])
    our_random_cell_num = int(args[1])
    opponent_board_num = our_random_cell_num
    opponent_cell_num = int(args[2])

    # Place our server generated random move
    place_mark(our_random_board_num, our_random_cell_num, Mark.PLAYER)
    # Place opponents move
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "next_move":
    opponent_board_num = global_next_board_num
    opponent_cell_num = int(args[0])

    # Place opponent move
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "win":
    print("Yay!! We win!! :)")
    return -1
  elif command == "loss":
    print("We lost :(")
    return -1
  elif command == "draw":
    print("Draw")
    return -1

  return 0

def main():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

  s.connect(('localhost', port))
  while True:
    text = s.recv(1024).decode()
    if not text:
      continue
    for cmd in text.split("\n"):
      response = parse_cmd(cmd)
      if response == -1:
        s.close()
        return
      elif response > 0:
        s.sendall((str(response) + "\n").encode())


if __name__ == "__main__":
  main()
