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
import random
import copy

from dataclasses import dataclass, field
from typing import List
from enum import Enum

class Mark(Enum):
  EMPTY = 0
  PLAYER = 1
  OPPONENT = 2

class Score(Enum):
  END = 1000
  REPEAT = 100
  BOARD_WINS = 50
  FORCE = 100
  TWO_MARKS = 4
  CENTRE = 2
  CORNER = 1
  EMPTY = 5
  DRAW = 0

  BLOCK = 6
  CAN_WINS = 25


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
global_prev_board_num = 0

#  . . . | . . . | . . .
#  . . . | . . . | . . .
#  . . O | . . . | . . .
#  ------+-------+------
#  . . . | . . . | . . .
#  . . . | . . . | . . .
#  . . . | . . . | X . .
#  ------+-------+------
#  . . . | X . . | . . .
#  . . . | . . . | . X .
#  . . O | . . . | . O X
def pc(i):
  global global_grid
  if global_grid[i] == Mark.EMPTY:
    return '.'
  elif global_grid[i] == Mark.PLAYER:
    return 'O'
  else:
    return 'X'

def print_board():
  global global_grid

  print(f" {pc(0)} {pc(1)} {pc(2)} | {pc(9)} {pc(10)} {pc(11)} | {pc(18)} {pc(19)} {pc(20)}")
  print(f" {pc(3)} {pc(4)} {pc(5)} | {pc(12)} {pc(13)} {pc(14)} | {pc(21)} {pc(22)} {pc(23)}")
  print(f" {pc(6)} {pc(7)} {pc(8)} | {pc(15)} {pc(16)} {pc(17)} | {pc(24)} {pc(25)} {pc(26)}")
  print(f" ------+-------+------")
  print(f" {pc(27)} {pc(28)} {pc(29)} | {pc(36)} {pc(37)} {pc(38)} | {pc(45)} {pc(46)} {pc(47)}")
  print(f" {pc(30)} {pc(31)} {pc(32)} | {pc(39)} {pc(40)} {pc(41)} | {pc(48)} {pc(49)} {pc(50)}")
  print(f" {pc(33)} {pc(34)} {pc(35)} | {pc(42)} {pc(43)} {pc(44)} | {pc(51)} {pc(52)} {pc(53)}")
  print(f" ------+-------+------")
  print(f" {pc(54)} {pc(55)} {pc(56)} | {pc(63)} {pc(64)} {pc(65)} | {pc(72)} {pc(73)} {pc(74)}")
  print(f" {pc(57)} {pc(58)} {pc(59)} | {pc(66)} {pc(67)} {pc(68)} | {pc(75)} {pc(76)} {pc(77)}")
  print(f" {pc(60)} {pc(61)} {pc(62)} | {pc(69)} {pc(70)} {pc(71)} | {pc(78)} {pc(79)} {pc(80)}")

def grid_coord(board_num, cell_num):
  global global_num_cells
  return (board_num - 1) * global_num_cells + (cell_num - 1)

def place_mark(board_num, cell_num, mark):
  global global_next_board_num
  global global_prev_board_num
  global global_grid

  coord = grid_coord(board_num, cell_num)

  global_grid[coord] = mark
  
  global_prev_board_num = board_num
  global_next_board_num = cell_num

# def make_move():
#   global global_grid
#   global global_next_board_num
# 
#   n = random.randint(1, 9)
#   coord = grid_coord(global_next_board_num, n)
#   while global_grid[coord] != Mark.EMPTY.value:
#     n = random.randint(1, 9)
#     coord = grid_coord(global_next_board_num, n)
# 
#   place_mark(global_next_board_num, n, Mark.PLAYER)
# 
#   return n

def could_win(grid, board, mark):
  row_indices = [[0,1,2],[0,2,1],[1,2,0],
                 [3,4,5],[3,5,4],[4,5,3],
                 [6,7,8],[6,8,7],[7,8,6]]
  for indexes in row_indices:
    i, j, k = indexes
    if board[i] == board[j] and board[i] != Mark.EMPTY and board[k] == Mark.EMPTY:
      if board[i] == mark:
        return True

  col_indices = [[0,3,6],[3,6,0],[0,6,3],
                 [1,4,7],[4,7,1],[1,7,4],
                 [2,5,8],[5,8,2],[2,8,5]]
  for indexes in col_indices:
    i, j, k = indexes
    if board[i] == board[j] and board[i] != Mark.EMPTY and board[k] == Mark.EMPTY:
      if board[i] == mark:
        return True

  diag_indices = [[0,4,8],[4,8,0],[0,8,4],
                  [6,4,2],[6,2,4],[4,2,6]]
  for indexes in diag_indices:
    i, j, k = indexes
    if board[i] == board[j] and board[i] != Mark.EMPTY and board[k] == Mark.EMPTY:
      if board[i] == mark:
        return True
   
  return False

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

def score_two_marks(board, are_max, is_next):
  score = 0
  
  next_mark = Mark.OPPONENT if are_max else Mark.PLAYER

  # 0 1 2
  # 3 4 5
  # 6 7 8
  # IMPORTANT: format is [m,m,e]
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
        if board[i] == Mark.PLAYER:
          if is_next and next_mark == Mark.PLAYER:
            score += Score.END.value 
          else:
            score += Score.TWO_MARKS.value 
            break
        elif board[i] == Mark.OPPONENT:
          if is_next and next_mark == Mark.OPPONENT:
            score -= Score.END.value 
          else:
            score -= Score.TWO_MARKS.value 
            break

  return score

def get_score(mark, score):
  if mark == Mark.PLAYER:
    return score
  elif mark == Mark.OPPONENT:
    return -score
  else:
    return 0

def score_positional(board):
  score = 0

  for i in [0, 2, 6, 8]:
    score += get_score(board[i], Score.CORNER.value)

  score += get_score(board[4], Score.CENTRE.value)

  return score

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
        if board[i] == m2 and board[k] == m1:
          score += get_score(board[k], Score.BLOCK.value)

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


def board_score(board, are_max, is_next):
  score += score_positional(board)

  if is_next:
    score += score_block(board, not are_max)
  else:
    score += score_block(board, are_max)

  score += score_two_marks(board, are_max, is_next)

  return score

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

def static_evaluation(grid, are_max, prev_move):
  evaluation = 0

  next_board_coord = grid_coord(prev_move.cell_num, 1)
  next_board = grid[next_board_coord:next_board_coord+9]
  if can_win(next_board, not are_max)[0]:
    if are_max:
      return -Score.END.value
    else:
      return Score.END.value

  # count how many times we have repeated cells
  m = Mark.PLAYER if are_max else Mark.OPPONENT
  for i in range(1, 10):
    cell_count = 0

    for j in range(1, 10):
      board_coord = grid_coord(j, i)
      if grid[board_coord] == m:
        cell_count += 1

    if cell_count >= 2:
      if are_max:
        return -Score.END.value
      else:
        return Score.END.value

  # constrain opponent
  # e_count = 0
  # for i in range(9):
  #   if next_board[i] == Mark.EMPTY:
  #     e_count += 1

  # if are_max:
  #   evaluation += (e_count * Score.EMPTY.value)
  # else:
  #   evaluation -= (e_count * Score.EMPTY.value)

  p_boards = 0
  o_boards = 0
  winnable_boards = []
  for i in range(1, 10):

    board_coord = grid_coord(i, 1)
    board = grid[board_coord:board_coord+9]

    if can_win(board, True)[0]:
      p_boards += 1
      if are_max:
        winnable_boards.append(i)
    elif can_win(board, False)[0]:
      o_boards += 1
      if not are_max:
        winnable_boards.append(i)

  if p_boards > o_boards:
    return Score.END.value
  #evaluation += Score.BOARD_WINS.value
  elif o_boards > p_boards:
    return -Score.END.value
    #evaluation -= Score.BOARD_WINS.value

  # if we have a board that we can win at, try and force opponent to pick it
  # if this move makes next board have cell vacant that we want opponent to pick, score high
  for i in winnable_boards:
    if next_board[i - 1] == Mark.EMPTY:
      if are_max:
        evaluation += Score.FORCE.value
      else:
        evaluation -= Score.FORCE.value

  cur_board_coord = grid_coord(prev_move.board_num, 1)
  cur_board = grid[cur_board_coord:cur_board_coord+9]
  evaluation += board_score(cur_board, are_max, False)

  return evaluation

def cell_counts(i):
  global global_grid
  cell_count = 0
  for j in range(1, 10):
    board_coord = grid_coord(j, i)
    if global_grid[board_coord] == Mark.PLAYER:
      cell_count += 1
  return cell_count

MAX_DEPTH = 8

def new_static(prev_move, are_max):
  score = 0

  #p_total_wins = 0
  #o_total_wins = 0
  #for i in range(1, 10):
  #  c = grid_coord(i, 1)
  #  b = global_grid[c:c+9]
  #  p_wins = Score.CAN_WINS.value * count_can_wins(b, True)
  #  o_wins = Score.CAN_WINS.value * count_can_wins(b, False)
  #  if i == prev_move.board_num:
  #    if are_max:
  #      p_total_wins += (4 * p_wins)
  #    else:
  #      o_total_wins += (4 * o_wins)
  #  else:
  #    p_total_wins += p_wins
  #    o_total_wins += o_wins
#
#  score += p_total_wins
#  score -= o_total_wins

  c = grid_coord(prev_move.board_num, 1)
  b = global_grid[c:c+9]
  score += Score.CAN_WINS.value * count_can_wins(b, True)
  score -= Score.CAN_WINS.value * count_can_wins(b, False)

  c = grid_coord(prev_move.board_num, 1)
  b = global_grid[c:c+9]
  m = Mark.PLAYER if are_max else Mark.OPPONENT
  if b[5] == m:
    if are_max:
      score += Score.CENTRE.value
    else:
      score -= Score.CENTRE.value

  score += score_block(b, are_max)

  return score

def minimax(grid, depth, are_max, cur_board_num, a, b, prev_move):
  if depth == MAX_DEPTH:
    return new_static(prev_move, are_max)
    #score = static_evaluation(grid, are_max, prev_move)
    #print(f"SCORE({prev_move.board_num}->{prev_move.cell_num}): {score}")
    #print_board()

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

  numbers = list(range(1, 10))
  random.shuffle(numbers)

  # 0 1 2
  # 3 4 5
  # 6 7 8
  numbers = [4,0,2,6,8,1,5,7,3]

  for i in numbers:
    if board[i] == Mark.EMPTY and not have_tie(grid, i+1):
      move = Move(board_num, i+1, 0)
      moves.append(move)
  return moves

  # moves = []
  # losable_moves = []

  # coord = grid_coord(board_num, 1)
  # board = grid[coord:coord+9]
  # 
  # for i in range(1, 10):
  #   if board[i-1] == Mark.EMPTY and not have_tie(grid, i):
  #     next_coord = grid_coord(i, 1)
  #     next_board = grid[next_coord:next_coord+9]
  #     # if we win
  #     if other_can_win(board, not are_max):
  #       return [Move(board_num, i, 0)]
  #     elif other_can_win(next_board, are_max):
  #       losable_moves.append(Move(board_num, i, 0))
  #     else:
  #       move = Move(board_num, i, 0)
  #       moves.append(move)

  # if len(moves) == 0:
  #   return losable_moves
  # else:
  #   return moves

def do_move(grid, move, are_max):
  mark = Mark.PLAYER if are_max else Mark.OPPONENT
  coord = grid_coord(move.board_num, move.cell_num) 
  grid[coord] = mark 

def undo_move(grid, move):
  coord = grid_coord(move.board_num, move.cell_num) 
  grid[coord] = Mark.EMPTY 

def get_counts(board):
  p_count = 0
  o_count = 0
  for i in range(9):
    if board[i] == Mark.PLAYER:
      p_count += 1
    elif board[i] == Mark.OPPONENT:
      o_count += 1

  return [p_count, o_count, 9 - p_count - o_count]


global_not_chosen_boards = [1,2,3,4,5,6,7,8,9]

def make_move():
  global global_grid
  global global_next_board_num 
  global global_prev_board_num 
  global global_not_chosen_boards

  board_coord = grid_coord(global_next_board_num, 1)
  board = global_grid[board_coord:board_coord+9]

  best_move = None

  w, i = can_win(board, True)
  # If can win, win
  if w:
    best_move = Move(global_next_board_num, i+1, 0)

  # Place on centre on empty board if first time
  #p, o, e = get_counts(board)
  #centre_board_coord = grid_coord(5, 1)
  #centre_board = global_grid[centre_board_coord:centre_board_coord+9]
  #cell_count = cell_counts(5)
  #if e == 9 and board[5] == Mark.EMPTY and cell_count == 0:
  #  best_move = Move(global_next_board_num, 5, 0)

  # Pick one haven't chosen yet
  #if best_move is None:
  #  for i in range(9):
  #    cell_count = cell_counts(i+1)
  #    if board[i] == Mark.EMPTY and cell_count == 0:
  #      best_move = Move(global_next_board_num, i+1, 0)
  #      break

  # Pick a can win if possible

  if best_move is None:
    for i in range(9):
      if global_grid[board_coord + i] == Mark.EMPTY:
        global_grid[board_coord + i] = Mark.PLAYER
        new_board = global_grid[board_coord:board_coord+9]

        c = grid_coord(i+1, 1)
        b = global_grid[c:c+9]
        if count_can_wins(new_board, True) > 0 and not can_win(b, False)[0]:
          best_move = Move(global_next_board_num, i+1, 0)
        
        global_grid[board_coord + i] = Mark.EMPTY


  # if p == 1, o == 1
  # lookup table 
  #for b in boards:
  #  if cur_board == b:
  #    move = .

  # Block opponent if possible
  #if best_move is None:
  #  w, i = can_win(board, False)
  #  if w:
  #    c = grid_coord(i+1, 1)
  #    b = global_grid[c:c+9]
  #    w_next, i_next = can_win(b, False)
  #    if not w_next:
  #      print(f"BLOCKED: {global_next_board_num},{i+1}")
  #      best_move = Move(global_next_board_num, i+1, 0)
  #    else:
  #      print(f"CAN'T BLOCK: {global_next_board_num},{i+1}")


  # if x centre, go in corner
  # if x on middle, go opposite
  # if x on corner

  # Put opponent on empty board
  #if best_move is None:
  #  for i in range(1, 10):
  #    if board[i-1] == Mark.EMPTY:
  #      c = grid_coord(i, 1)
  #      b = global_grid[c:c+9]
  #      p, o, e = get_counts(b)
  #      if e == 9: 
  #        best_move = Move(global_next_board_num, i, 0)
  #        break

  # Force opponent back into same grid if possible
  #if best_move is None:
  #  prev_board_coord = grid_coord(global_prev_board_num, 1)
  #  prev_board = global_grid[prev_board_coord:prev_board_coord+9]
  #  if board[global_prev_board_num - 1] == Mark.EMPTY and not can_win(prev_board, False)[0]:
  #    best_move = Move(global_next_board_num, global_prev_board_num, 0)



  # See if can pick centre or corners
  #if best_move is None:
  #  for i in [4, 3, 6, 8, 0]:
  #    c = grid_coord(i+1, 1)
  #    b = global_grid[c:c+9]
  #    if board[i] == Mark.EMPTY and not can_win(b, False)[0]:
  #      best_move = Move(global_next_board_num, i+1, 0)
  #      break

  ## Resort to doing any move that doesn't lose 
  #if best_move is None:
  #  for i in range(1, 10):
  #    if board[i-1] == Mark.EMPTY:
  #      c = grid_coord(i, 1)
  #      b = global_grid[c:c+9]
  #      if not can_win(b, False)[0]:
  #        best_move = Move(global_next_board_num, i, 0)
  #        break
  # best_move = minimax(global_grid, 0, True, global_next_board_num, Score.MIN_SCORE.value, Score.MAX_SCORE.value, None)
    #print("MINIMAX")
  if best_move is None:
    print("MINIMAX")
    best_move = minimax(global_grid, 0, True, global_next_board_num, Score.MIN_SCORE.value, Score.MAX_SCORE.value, None)
  #print(f"BEST: {best_move.score}")

  place_mark(global_next_board_num, best_move.cell_num, Mark.PLAYER)

  print_board()
  print(f"Moved: {best_move.board_num}, {best_move.cell_num}")

  return best_move.cell_num


global_moves_to_choose = []

def parse_cmd(cmd):
  if "(" in cmd:
    command, args = cmd.split("(")
    args = args.split(")")[0]
    args = args.split(",")
  else:
    command, args = cmd, []

  print(f"{command}, {args}")

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
    print_board()
    return -1
  elif command == "loss":
    print("We lost :(")
    print_board()
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
