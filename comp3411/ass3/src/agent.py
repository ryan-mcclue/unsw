#!/usr/bin/python3
# SPDX-License-Identifier: zlib-acknowledgement

#################################################################
## QUESTION ANSWER ##############################################
#################################################################
## DATA STRUCTURES:
# * Mark enum:
#   Provides a readable encoding of a possible value for a tic-tac-toe board cell
# * Score enum:
#   Encodes a value to assign to a particular metric that's used in computing a static evaluation score:
#     - END indicates victory and is assigned the highest value to encourage agent to win.
#     - BLOCK is if a mark impedes the direction of opposing marks.
#       It's assigned the next highest value to encourage agent to block opponent winning the game.
#     - TWO_MARKS is for two marks, whereby if a third mark were made in that direction, the game would end.
#     - CENTRE is assigned for marks that are in the centre of the board.
#       The centre is most powerful cell to play on as it connects many directions. 
#       So, it's given a higher score than corner cells.
#     - CORNER is assigned for marks that are in corners of board
#     - DRAW is if game is drawn, i.e. no possible moves
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
#   A possible move is one where that cell is empty on the current board and that the resulting next board is not full.
#   For each move, first check if it has won for the player or opponent and return the END score value.
#   Otherwise recurse on minimax for this move.
#   Only at depth 0, i.e. the first iteration of minimax is the move appended to the score.
#   This is because we only want to initial move to be played, not any of the sub-moves whose state are used to calculate the score.
#   If maximising, then take maximum of all scores for this tree depth, otherwise minimum.
#   If at MAX_DEPTH a static evaluation is performed on the board state.
#   The score for the current board is evaluated as per the Score enum fields.
#   However, the score for the next board that the move would result in is also calculated.
#   In this case, if there are two marks and a corresponding empty slot, then this means that the current move would allow the opponent to win on their next turn.
#   So, the evaluation function registers this as a END score instead of a TWO_MARKS score.
#   The static evaluation function is symmetric, meaning its run equally for both players. 
#   This ensures each move takes into account other player.
#   These scores are combined for a more robust evaluation.
#   Based on the optimal move returned by minimax, a mark is placed on the board.
#   When a mark is placed, the global_active_board_num variable is updated to the cell number chosen.

import sys
import socket
import copy

from dataclasses import dataclass
from typing import List
from enum import Enum

class Mark(Enum):
  EMPTY = 0
  PLAYER = 1
  OPPONENT = 2

class Score(Enum):
  END = 1000
  BLOCK = 6
  CAN_WINS = 25
  BOARD_WINS = 50
  CENTRE = 2
  DRAW = 0

  WINNABLE_EMPTY = 25

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

def score_block(board, are_max):
  score = 0

  m1 = Mark.PLAYER if are_max else Mark.OPPONENT
  m2 = Mark.OPPONENT if are_max else Mark.PLAYER

  # 0 1 2
  # 3 4 5
  # 6 7 8
  # IMPORTANT: format is [m2,m2,m1]
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
      if board[i] == board[j]:
        # Blocking opponent
        if board[i] == Mark.OPPONENT and board[k] == Mark.PLAYER:
          score += Score.BLOCK.value 
        # Blocking player
        elif board[i] == Mark.PLAYER and board[k] == Mark.OPPONENT:
          score -= Score.BLOCK.value 

  return score


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

def get_empty_cells(b):
  e = []

  for i in range(1,10):
    if b[i-1] == Mark.EMPTY:
      e.append(i)

  return e

def winnable_boards(grid, are_max):
  winnable_boards = []
  for i in range(1, 10):
    c = grid_coord(i, 1)
    b = grid[c:c+9]
    if can_win(b, are_max)[0]:
      winnable_boards.append(i)

  return winnable_boards

def static_evaluation(grid, prev_move, are_max):
  # First evaluate whole board and see how many are favourable
  p_wins = 0
  o_wins = 0
  o_greater_than_p = 0
  p_greater_than_o = 0
  for i in range(1, 10):
    c = grid_coord(i, 1)
    b = grid[c:c+9]
    p_can_wins = count_can_wins(b, True)
    o_can_wins = count_can_wins(b, False)
    p, o, e = get_counts(b)
    
    if p > o:
      p_greater_than_o += 1
    if o > p:
      o_greater_than_p += 1

    if p > 0 and o == 0:
      p_wins += 1
    elif o > 0 and p == 0:
      o_wins += 1
    elif p_can_wins > 0 and p >= o: 
      p_wins += 1
    elif o_can_wins > 0 and o >= p:
      o_wins += 1

  if o_greater_than_p - p_greater_than_o > 1:
    return -Score.END.value
  elif p_greater_than_o - o_greater_than_p > 1:
    return Score.END.value
  
  # Evaluate this board score to differentiate between favourable  
  score = 0
  c = grid_coord(prev_move.board_num, 1)
  b = grid[c:c+9]

  #e = get_empty_cells(b) 
  #pb_wins = winnable_boards(grid, True)
  #ob_wins = winnable_boards(grid, False)
  #p_empty = any(c in pb_wins for c in e)
  #o_empty = any(c in ob_wins for c in e)
  #if are_max and not p_empty:
  #  return -Score.END.value
  #elif not are_max and not o_empty:
  #  return Score.END.value

  if count_can_wins(b, True):
    score += Score.CAN_WINS.value
  elif count_can_wins(b, False):
    score -= Score.CAN_WINS.value

  #if are_max and b[5] == Mark.PLAYER:
  #  score += Score.CENTRE.value
  #if not are_max and b[5] == Mark.OPPONENT:
  #  score -= Score.CENTRE.value
  score += score_block(b, are_max)

  if o_wins > p_wins:
    return -Score.END.value
  elif p_wins > o_wins:
    return Score.END.value
  else:
    return score

def minimax(grid, depth, are_max, cur_board_num, a, b, prev_move):
  if depth == MAX_DEPTH:
    return static_evaluation(grid, prev_move, are_max)

  scores = []

  possible_moves = get_possible_moves(grid, cur_board_num, are_max)

  for move in possible_moves:
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
          score = -Score.END.value
        else:
          score = Score.END.value
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

  # if a draw
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


def have_tie(grid, board_num):
  coord = grid_coord(board_num, 1)
  for i in range(9):
    if grid[coord + i] == Mark.EMPTY:
      return False
  return True

def get_possible_moves(grid, board_num, are_max):
  moves = []
  coord = grid_coord(board_num, 1)
  board = grid[coord:coord+9]

  # 0 1 2
  # 3 4 5
  # 6 7 8
  numbers = [4,0,2,6,8,1,5,7,3]

  for i in numbers:
    if board[i] == Mark.EMPTY and not have_tie(grid, i+1):
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
  global global_prev_board_num 

  board_coord = grid_coord(global_next_board_num, 1)
  board = global_grid[board_coord:board_coord+9]

  best_move = None

  w, i = can_win(board, True)
  # If can win, win
  if w:
    best_move = Move(global_next_board_num, i+1, 0)

  # Pick a can win if possible
  #if best_move is None:
  #  for i in range(9):
  #    if global_grid[board_coord + i] == Mark.EMPTY:
  #      global_grid[board_coord + i] = Mark.PLAYER
  #      new_board = global_grid[board_coord:board_coord+9]

  #      c = grid_coord(i+1, 1)
  #      b = global_grid[c:c+9]
  #      if count_can_wins(new_board, True) > 0 and not can_win(b, False)[0]:
  #        best_move = Move(global_next_board_num, i+1, 0)
  #      
  #      global_grid[board_coord + i] = Mark.EMPTY


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
    # going second, i.e. 'o'
    opponent_board_num = int(args[0])
    opponent_cell_num = int(args[1])

    # place server generated random move for opponent
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "third_move":
    # going first, i.e. 'x'
    our_random_board_num = int(args[0])
    our_random_cell_num = int(args[1])
    opponent_board_num = our_random_cell_num
    opponent_cell_num = int(args[2])

    # place our server generated random move
    place_mark(our_random_board_num, our_random_cell_num, Mark.PLAYER)
    # place opponents move
    place_mark(opponent_board_num, opponent_cell_num, Mark.OPPONENT)

    return make_move()
  elif command == "next_move":
    opponent_board_num = global_next_board_num
    opponent_cell_num = int(args[0])

    # place opponent move
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
  port = 0
  if sys.gettrace():
    port = 12345
  else:
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
